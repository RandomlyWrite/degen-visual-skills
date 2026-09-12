#!/usr/bin/env python3
"""
Degen Sticker Pipeline — Core
The ruthless single-clip green-screen to Telegram WebM converter.
See SKILL.md for full docs and the batch + enforcer companions.
"""

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Optional


def probe_media(input_path: Path) -> dict:
    cmd = [
        "ffprobe", "-v", "error",
        "-show_format", "-show_streams", "-of", "json", str(input_path)
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return json.loads(result.stdout)


def process_green_screen_to_sticker(
    input_video: str,
    output_webm: Optional[str] = None,
    target_size: int = 512,
    max_duration_s: float = 3.0,
    bitrate: str = "200K",
    chromakey_color: str = "0x00FF00",
    similarity: float = 0.10,
    blend: float = 0.20,
    fps: int = 30,
    overwrite: bool = False,
    verbose: bool = False
) -> str:
    """
    Core pipeline. See SKILL.md for usage and the dark truth behind every flag.
    """
    input_path = Path(input_video).resolve()
    if not input_path.exists():
        raise FileNotFoundError(f"Input video not found: {input_path}")

    if output_webm is None:
        output_webm = str(input_path.with_suffix(".webm"))
    output_path = Path(output_webm).resolve()

    if output_path.exists() and not overwrite:
        raise FileExistsError(
            f"Output already exists: {output_path}. "
            "Pass overwrite=True or choose a different path."
        )

    try:
        probe = probe_media(input_path)
        duration = float(probe.get("format", {}).get("duration", 0))
        if verbose:
            print(f"[INFO] Input duration: {duration:.2f}s")
        if duration > max_duration_s + 0.5:
            print(f"[WARN] Input {duration:.2f}s will be trimmed to {max_duration_s}s from start.")
    except Exception as e:
        if verbose:
            print(f"[WARN] Probe failed: {e}. Proceeding...")

    tmp_dir = Path(tempfile.mkdtemp(prefix="degen_sticker_"))
    tmp_output = tmp_dir / f"{input_path.stem}_processed.webm"

    try:
        vf_filter = (
            f"chromakey={chromakey_color}:{similarity}:{blend},"
            f"scale={target_size}:{target_size}:force_original_aspect_ratio=decrease,"
            f"fps={fps}"
        )

        cmd = [
            "ffmpeg", "-n",
            "-i", str(input_path),
            "-vf", vf_filter,
            "-c:v", "libvpx-vp9",
            "-b:v", bitrate,
            "-pix_fmt", "yuva420p",
            "-auto-alt-ref", "0",
            "-an",
            "-t", str(max_duration_s),
            str(tmp_output)
        ]

        if verbose:
            print(f"[CMD] {' '.join(cmd)}")

        subprocess.run(cmd, check=True, capture_output=not verbose, text=True)

        if not tmp_output.exists():
            raise RuntimeError("FFmpeg produced no output.")

        verify_cmd = ["ffprobe", "-v", "error", "-show_format", str(tmp_output)]
        subprocess.run(verify_cmd, check=True, capture_output=True)

        if output_path.exists() and overwrite:
            output_path.unlink()

        shutil.move(str(tmp_output), str(output_path))

        if verbose:
            size_kb = output_path.stat().st_size / 1024
            print(f"[SUCCESS] Forged: {output_path} ({size_kb:.1f} KB)")

        return str(output_path)

    except subprocess.CalledProcessError as e:
        stderr = e.stderr.decode() if isinstance(e.stderr, bytes) else str(e.stderr)
        raise RuntimeError(
            f"FFmpeg failed (code {e.returncode}).\n"
            f"Try adjusting similarity/blend or ensure solid #00FF00 green plate.\n"
            f"Stderr snippet: {stderr[:500]}"
        ) from e
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)


def main():
    parser = argparse.ArgumentParser(description="Core degen sticker single-file processor")
    parser.add_argument("input_video")
    parser.add_argument("output_webm", nargs="?", default=None)
    parser.add_argument("--overwrite", "-y", action="store_true")
    parser.add_argument("--verbose", "-v", action="store_true")
    parser.add_argument("--similarity", type=float, default=0.10)
    parser.add_argument("--blend", type=float, default=0.20)
    args = parser.parse_args()

    try:
        result = process_green_screen_to_sticker(
            input_video=args.input_video,
            output_webm=args.output_webm,
            similarity=args.similarity,
            blend=args.blend,
            overwrite=args.overwrite,
            verbose=args.verbose
        )
        print(result)
    except Exception as e:
        print(f"[FATAL] {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

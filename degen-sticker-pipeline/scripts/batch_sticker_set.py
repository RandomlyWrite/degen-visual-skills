#!/usr/bin/env python3
"""
Batch Sticker Set Forger
========================
Takes a folder of green-screen MP4 clips and forges a complete Telegram-ready
animated sticker set:
- Processes every qualifying .mp4 through the core degen pipeline
- Outputs clean .webm files (named cleanly)
- Auto-generates a static cover thumbnail PNG (512x512) from a hero clip
  (first file or one you specify)
- Writes a simple manifest.json for your records or bot upload logic

This turns "I have 8 green-screen character animations" into
"here is my ready-to-upload sticker set folder" in one command.

Usage (Python):
    from batch_sticker_set import forge_sticker_set
    forge_sticker_set(
        input_folder="green_clips/",
        output_folder="my_sticker_set/",
        hero_clip="spade_queen_v3_green.mp4",  # optional, defaults to first
        verbose=True
    )

CLI:
    python batch_sticker_set.py green_clips/ my_sticker_set/ --hero spade_queen_v3_green.mp4 -v
"""

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import List, Optional

# Import the core processor (assumes same scripts/ dir)
try:
    from degen_sticker_pipeline import process_green_screen_to_sticker
except ImportError:
    # Fallback for direct CLI runs
    sys.path.insert(0, str(Path(__file__).parent))
    from degen_sticker_pipeline import process_green_screen_to_sticker


def extract_thumbnail(
    video_path: Path,
    output_png: Path,
    timestamp: str = "00:00:01",
    size: int = 512
) -> Path:
    """Extract a single high-quality frame as cover thumbnail."""
    cmd = [
        "ffmpeg", "-y",
        "-ss", timestamp,
        "-i", str(video_path),
        "-frames:v", "1",
        "-vf", f"scale={size}:{size}:force_original_aspect_ratio=decrease",
        "-q:v", "2",
        str(output_png)
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    return output_png


def forge_sticker_set(
    input_folder: str,
    output_folder: str,
    hero_clip: Optional[str] = None,
    similarity: float = 0.10,
    blend: float = 0.20,
    overwrite: bool = False,
    verbose: bool = False
) -> dict:
    """
    Main batch function. Returns a dict with processed files and cover path.
    """
    in_dir = Path(input_folder).resolve()
    out_dir = Path(output_folder).resolve()

    if not in_dir.exists():
        raise FileNotFoundError(f"Input folder not found: {in_dir}")

    out_dir.mkdir(parents=True, exist_ok=True)

    # Collect candidate clips (prefer *_green.mp4 naming, fall back to any .mp4)
    clips = sorted(list(in_dir.glob("*_green.mp4")) + list(in_dir.glob("*.mp4")))
    # Deduplicate while preserving order
    seen = set()
    unique_clips = []
    for c in clips:
        if c.name not in seen:
            seen.add(c.name)
            unique_clips.append(c)

    if not unique_clips:
        raise FileNotFoundError(f"No .mp4 files found in {in_dir}")

    if verbose:
        print(f"[INFO] Found {len(unique_clips)} candidate clips")

    processed = []
    for clip in unique_clips:
        out_name = clip.stem.replace("_green", "") + ".webm"
        out_path = out_dir / out_name
        try:
            result = process_green_screen_to_sticker(
                input_video=str(clip),
                output_webm=str(out_path),
                similarity=similarity,
                blend=blend,
                overwrite=overwrite,
                verbose=verbose
            )
            processed.append({"source": clip.name, "output": out_name, "path": result})
            if verbose:
                print(f"[OK] {clip.name} → {out_name}")
        except Exception as e:
            print(f"[FAIL] {clip.name}: {e}", file=sys.stderr)

    # Hero clip for cover
    hero_path = None
    if hero_clip:
        # Try input first, then output
        candidate = in_dir / hero_clip
        if not candidate.exists():
            candidate = out_dir / hero_clip
        if candidate.exists():
            hero_path = candidate
        else:
            # Try matching stem
            for p in processed:
                if hero_clip in p["source"] or hero_clip in p["output"]:
                    hero_path = Path(p["path"])
                    break
    if hero_path is None and processed:
        # Default to first processed
        hero_path = Path(processed[0]["path"])

    cover_path = out_dir / "cover.png"
    try:
        if hero_path and hero_path.suffix.lower() == ".webm":
            extract_thumbnail(hero_path, cover_path, timestamp="00:00:00.5")
        elif hero_path:
            extract_thumbnail(hero_path, cover_path, timestamp="00:00:01")
        if verbose and cover_path.exists():
            print(f"[COVER] Generated {cover_path}")
    except Exception as e:
        print(f"[WARN] Could not generate cover thumbnail: {e}", file=sys.stderr)
        cover_path = None

    # Manifest
    manifest = {
        "sticker_set_name": out_dir.name,
        "total_stickers": len(processed),
        "cover": str(cover_path) if cover_path and cover_path.exists() else None,
        "stickers": processed,
        "notes": "Ready for upload via @stickers bot or Telegram API. Use cover.png as the set icon."
    }

    manifest_path = out_dir / "sticker_set_manifest.json"
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)

    if verbose:
        print(f"[MANIFEST] Wrote {manifest_path}")
        print(f"[DONE] Sticker set forged in {out_dir} with {len(processed)} stickers + cover.")

    return manifest


def main():
    parser = argparse.ArgumentParser(description="Batch forge a full Telegram animated sticker set from green-screen clips")
    parser.add_argument("input_folder", help="Folder containing your *_green.mp4 clips")
    parser.add_argument("output_folder", help="Where to write the processed .webm set + cover.png + manifest")
    parser.add_argument("--hero", "-H", default=None, help="Filename of the hero clip to use for cover thumbnail (in input or output folder)")
    parser.add_argument("--overwrite", "-y", action="store_true")
    parser.add_argument("--verbose", "-v", action="store_true")
    parser.add_argument("--similarity", type=float, default=0.10)
    parser.add_argument("--blend", type=float, default=0.20)
    args = parser.parse_args()

    try:
        result = forge_sticker_set(
            input_folder=args.input_folder,
            output_folder=args.output_folder,
            hero_clip=args.hero,
            similarity=args.similarity,
            blend=args.blend,
            overwrite=args.overwrite,
            verbose=args.verbose
        )
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"[FATAL] {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

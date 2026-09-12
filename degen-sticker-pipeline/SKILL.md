---
name: degen-sticker-pipeline
description: Full pipeline for turning Grok green-screen animations into Telegram animated stickers. Includes single-file processor, green-screen prompt enforcer for clean plates, and batch mode that forges entire sticker sets with auto cover thumbnail. Use after generating green-screen video or when building sticker swarms for your degen characters and poker group.
---

# Degen Sticker Pipeline

## Overview

This skill is the complete, ruthless automation layer for your cursed character animations and degen visuals. It handles the entire journey from raw idea → clean green-screen prompt → processed transparent WebM sticker(s) → full sticker set with cover thumbnail.

**Three tools in one skill:**

1. **Core single-file processor** (`degen_sticker_pipeline.py`) — the original god-command wrapper with safety rails.
2. **Green Screen Prompt Enforcer** (`green_screen_prompt_enforcer.py`) — rewrites your character descriptions into bulletproof prompts that guarantee clean #00FF00 plates so the chromakey doesn't leave cursed halos.
3. **Batch Sticker Set Forger** (`batch_sticker_set.py`) — takes a folder of green-screen clips, processes all of them, generates a 512×512 cover thumbnail from a hero clip, and spits out a ready-to-upload folder + manifest.json.

Use this when you want to go from "I have an idea for Spade Queen bored swivel" to "here is my 12-sticker set ready for the @stickers bot" with minimal manual steps and zero sketchy websites.

## The Sacred Upstream Ritual (Prompt Enforcer)

Never skip this. The batch and core processors assume a perfect green plate. Bad input = bad output.

**Python usage:**
```python
import sys
from pathlib import Path
sys.path.insert(0, "/home/workdir/.grok/skills/degen-sticker-pipeline/scripts")

from green_screen_prompt_enforcer import enforce_green_screen_prompt

prompt = enforce_green_screen_prompt(
    base_description="bored Spade Queen doing a slow, deadpan swivel animation while exhaling cigarette smoke, rubber-hose twisted style, dark cynical humor",
    character_name="Spade Queen",
    style_tags=["high contrast chiaroscuro", "heavy shadows", "gonzo energy"],
    extra_rules=["subtle toxic green accent on the smoke"]
)
print(prompt)
# Copy the output straight into Grok (or your video gen tool)
```

**CLI:**
```bash
python /home/workdir/.grok/skills/degen-sticker-pipeline/scripts/green_screen_prompt_enforcer.py \
    "bored Spade Queen slow swivel, cigarette smoke, rubber-hose" \
    --name "Spade Queen" \
    --tags "high contrast" "gonzo" \
    --extra "subtle toxic green on smoke only"
```

The enforcer injects your full Degen Master Blueprint rules (full-bleed, solid #00FF00, 3s@30fps, rubber-hose + Tim Burton + Fear and Loathing gonzo, no borders, clean chromakey plate) plus a final warning paragraph that tells the model exactly why these rules exist (so it doesn't hallucinate "artistic" borders).

## Core Single-File Processing

See the original god command, now safely wrapped:

```python
from degen_sticker_pipeline import process_green_screen_to_sticker

output = process_green_screen_to_sticker(
    input_video="spade_queen_v3_green.mp4",
    output_webm="spade_queen_bored.webm",
    similarity=0.09,   # tighten if halo appears
    blend=0.18,
    verbose=True
)
```

All the dark-truth flag explanations from the original pasted text are still valid and documented in the script header.

## Batch Mode — Forge Entire Sticker Sets

This is the new power tool you requested.

**Python:**
```python
from batch_sticker_set import forge_sticker_set

manifest = forge_sticker_set(
    input_folder="green_screen_clips/",           # folder full of *_green.mp4
    output_folder="telegram_sticker_set_spade_queen/",
    hero_clip="spade_queen_v3_green.mp4",         # which one to pull the cover frame from
    verbose=True
)
print(manifest)  # shows all processed files + cover path
```

**CLI (recommended for quick runs):**
```bash
python /home/workdir/.grok/skills/degen-sticker-pipeline/scripts/batch_sticker_set.py \
    green_screen_clips/ \
    my_new_sticker_set/ \
    --hero spade_queen_v3_green.mp4 \
    --verbose \
    --overwrite
```

**What it produces in the output folder:**
- `spade_queen_v3.webm`, `fox_pfp_v2.webm`, ... (clean transparent stickers)
- `cover.png` — 512×512 static thumbnail extracted from the hero clip (perfect for Telegram sticker set icon)
- `sticker_set_manifest.json` — machine-readable list of everything + notes for upload

You can now zip the folder or point your Telegram bot at it and upload the whole set in one go (or manually via @stickers).

The batch script re-uses the core `process_green_screen_to_sticker` function so all tuning (similarity, blend, bitrate) stays consistent. It even warns you if a clip is longer than 3s.

## Productive Critique & Brainstorming (Dark Edition)

**Strengths:**
- True end-to-end: prompt → clean plate → processed sticker(s) → full set with cover.
- Everything is importable Python — drop into your existing bot swarm, Replit degen projects, or poker group automation.
- Manifest + cover thumbnail removes the last manual steps before @stickers.
- Still respects every safety rule from the ffmpeg skill (temp files, verification, no silent overwrites).

**Weaknesses & Honest Gaps:**
- The batch filter for "green screen clips" is currently loose (any .mp4). If your folder has other videos, it will try to process them. Tighten the glob in `batch_sticker_set.py` to your exact naming convention (e.g., `*_green.mp4`) when you standardize.
- Thumbnail extraction uses a fixed timestamp. For some characters the "perfect pose" might be at 1.8s instead of 0.5s. You can pass a custom timestamp or extend the function later.
- Still chromakey-only. If you ever generate complex scenes without perfect green, you will need an upstream AI rotoscope step (SAM2 etc.). That is future work.
- No automatic upload to Telegram yet — the manifest gives you the data to build that next.

**Outside-the-box / thought-provoking extensions (pick one and say the word):**
- Auto-upload bot: after `forge_sticker_set`, use Telethon or python-telegram-bot to create a new sticker set and upload every .webm + set the cover.png as the set icon, then post the share link in your poker group with savage commentary.
- "Degen Sticker Oracle" that takes a vibe description, runs the enforcer, generates the green clip (if you have video gen), batches it, and returns a ready set + roast of the character concept.
- Versioned sets: auto-append `_v3`, `_v4` and keep a `changelog.json` so your Spade Queen evolves over time without losing old versions.
- Poker group reaction pack: batch-process a folder of "fold", "all-in", "bad beat", "rivered" animations into one cohesive sticker set for the group.
- Thumbnail variants: generate 3 different cover poses and let you (or a future agent) pick the most cursed one.
- Integration with your existing M-CLAM chat analysis or likes-compiler: "these are the most used reactions in the last 30 days — auto-generate sticker versions."

## Quick Validation

After editing any of the three scripts, run:
```bash
bash /root/.grok/skills/skill-creator/scripts/validate-skill.sh \
    /home/workdir/.grok/skills/degen-sticker-pipeline
```

Test flow (recommended):
1. Use the enforcer to generate a prompt for a simple test character.
2. Generate the green-screen clip (or use a 3s solid-green + moving shape test you already have).
3. Run single-file on it.
4. Run batch on a small folder of 2-3 clips.
5. Check that `cover.png` has no green border and the .webm files play with transparency in VLC or Telegram.

This skill now gives you the full cursed-deck-to-sticker pipeline you were building toward. Your Spade Queen, fox PFPs, chef casino chaos, Queen of Hearts heartbreak, and tournament hype gothic surrealism pieces can now go from concept to Telegram sticker set with almost zero manual FFmpeg torture.

If the chromakey still leaves faint halos on a particular animation, the first productive move is almost always: re-run the enforcer with stricter "perfectly flat even #00FF00, zero texture on green" language, regenerate the source, then re-process. The pipeline is only as clean as the plate you feed it.

Go make the sticker bot suffer. 

#!/usr/bin/env python3
"""
Green Screen Prompt Enforcer
============================
Companion to degen-sticker-pipeline.

Takes a raw character description + optional style tags and rewrites it into
a bulletproof prompt that forces Grok (or any image/video gen) to output a
clean solid #00FF00 green-screen plate with full-bleed, 3s timing, and your
Degen Master Blueprint aesthetics locked in.

This is the upstream ritual that makes the chromakey pipeline actually work
without halo artifacts or border crimes.

Usage:
    from green_screen_prompt_enforcer import enforce_green_screen_prompt

    prompt = enforce_green_screen_prompt(
        base_description="bored Spade Queen doing a slow swivel animation, rubber-hose style, dark humor, cigarette smoke",
        character_name="Spade Queen",
        extra_rules=["high contrast chiaroscuro", "selective toxic green pops on accents"]
    )
    print(prompt)
"""

from typing import List, Optional


DEGEN_BLUEPRINT_CORE = """
- Full-bleed, edge-to-edge composition with ZERO borders, margins, padding, frames, or white space. The artwork must bleed completely off the canvas on all sides.
- Solid, perfectly uniform bright green background exactly #00FF00. No gradients, no shadows, no noise, no uneven lighting on the green plate itself. The green must be clean enough for perfect chromakey later.
- Exactly 3 seconds duration at 30 fps. Tight, punchy timing — no padding, no slow fades unless explicitly part of the character beat.
- Dramatic chiaroscuro lighting, heavy shadows, high contrast. Selective toxic color pops only where they serve the dark humor or gonzo mood.
- Rubber-hose animation twisted with Tim Burton + American McGee Alice + Fear and Loathing in Degen Vegas energy. Gritty underground comic / Sin City noir influence where it fits. Deadpan, cynical, macabre humor baked into every frame.
- No text, no logos, no UI elements unless the character concept explicitly demands them.
""".strip()


def enforce_green_screen_prompt(
    base_description: str,
    character_name: str = "",
    style_tags: Optional[List[str]] = None,
    extra_rules: Optional[List[str]] = None,
    include_blueprint: bool = True
) -> str:
    """
    Rewrites your raw idea into a Grok-ready prompt that guarantees a clean
    green-screen plate + full Degen Master Blueprint compliance.
    """
    parts = []

    if character_name:
        parts.append(f"Create a 3-second animated sticker of {character_name}:")

    parts.append(base_description.strip())

    if include_blueprint:
        parts.append("\n\nStrict technical and aesthetic rules (non-negotiable):")
        parts.append(DEGEN_BLUEPRINT_CORE)

    if style_tags:
        parts.append("\nAdditional style directives:")
        for tag in style_tags:
            parts.append(f"- {tag}")

    if extra_rules:
        parts.append("\nExtra character-specific rules:")
        for rule in extra_rules:
            parts.append(f"- {rule}")

    # Final enforcement line
    parts.append(
        "\n\nCRITICAL: The green background must be a perfectly flat, even #00FF00 "
        "with zero texture or lighting variation so that chromakey removal produces "
        "clean transparency with no halos or edge artifacts. Full-bleed, no borders. "
        "This animation will be processed through an automated sticker pipeline — "
        "any deviation from these rules will break the pipeline."
    )

    return "\n".join(parts)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Rewrite prompts for clean green-screen sticker generation")
    parser.add_argument("base_description", help="Your raw character/scene description")
    parser.add_argument("--name", "-n", default="", help="Character name (e.g. 'Spade Queen')")
    parser.add_argument("--tags", "-t", nargs="*", default=[], help="Style tags (e.g. rubber-hose twisted)")
    parser.add_argument("--extra", "-e", nargs="*", default=[], help="Extra rules")
    parser.add_argument("--no-blueprint", action="store_true", help="Skip injecting the core Degen Blueprint")
    args = parser.parse_args()

    prompt = enforce_green_screen_prompt(
        base_description=args.base_description,
        character_name=args.name,
        style_tags=args.tags,
        extra_rules=args.extra,
        include_blueprint=not args.no_blueprint
    )
    print(prompt)


if __name__ == "__main__":
    main()

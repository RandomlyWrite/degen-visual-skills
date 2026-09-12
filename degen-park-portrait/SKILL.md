---
name: degen-park-portrait
description: Use to transform uploaded reference photos into consistent South Park style Degen Park characters with extreme Stan/Kyle proportions — massively oversized head (45-55%), very short compact torso, very short thick limbs, almost baby-like squat proportions. Supports middle finger pose, custom props, and different Degen Park locations. Exact feature fidelity, 2048x2048 output. Triggers on degen park portrait, south park degen, degen park edit, make degen park version of photo, illustrate in degen park style, degen park character, group shot, add prop to character.
---

# Degen Park Portrait Framework

When the user uploads one or more reference photos and invokes this skill, follow this exact process for reproducible, high-consistency results.

## South Park Visual Style Rules (Important)

South Park uses a very specific aesthetic that mimics construction paper cutouts:

- **Bold black outlines** around all shapes
- **Flat colors** with minimal to no shading or gradients
- **Simple geometric shapes** (heads are often near-perfect circles or ovals)
- **Limited detail** — characters are built from basic forms rather than realistic anatomy
- **Construction paper / cutout feel** — even in digital work, the style avoids realistic textures and lighting

**Recommended style anchor phrase** (use in all prompts):  
"precise South Park 2D animation style, construction paper cutout aesthetic, bold black outlines, flat colors, minimal shading, simple geometric shapes, by Matt Stone and Trey Parker"

## South Park Proportion Rules (Critical) — Updated

South Park characters follow very extreme, exaggerated proportions. This skill now defaults to **Stan/Kyle-style baby-like proportions**:

- **Head Size**: Extremely large — **45-55% of total height** (the single most important element)
- **Torso**: Very short and compact
- **Limbs (Arms & Legs)**: Very short and thick/stubby
- **Overall Feel**: Almost baby-like or extremely squat cartoon proportions — never realistic adult human proportions
- **Golden Rule**: If the character starts looking like a normal adult human, the proportions are wrong. Force the classic exaggerated "big head, tiny body" Stan/Kyle look.

**Recommended phrasing** (copy-paste into prompts when needed):  
"extremely exaggerated South Park proportions: massively oversized head (45-55% of height), very short compact torso, very short thick stubby arms and legs, almost baby-like squat stature exactly like Stan or Kyle from South Park"

## Step 1: Analyze uploads
- Identify every distinct character or subject photo.
- If a clean "Degen Park" background image is also uploaded, note its image_id (use it for higher-fidelity background replacement when possible).
- Note any requests for group shot, props, or specific Degen Park location.

## Step 2: Portrait Mode (default for single or multiple individuals)
For **each** character reference photo, output a `render_edited_image` component.

**Refined Master Prompt Template** (customize only the bracketed sections):

Replace ONLY the background with the exact clean empty Degen Park scene: snowy ground in foreground, wooden sign on the left reading "DEGEN PARK" in black carved letters, green pine trees, snow-capped mountains in the distance, blue sky with white clouds, no other signs, crosses, buildings or objects. Keep the foreground character **100% identical** in every visible detail from the reference photo: [face shape and expression, hair style/color/length, facial hair or lack thereof, skin details, eyes, exact accessories like earrings/nose ring/dog tags/hat logo, clothing with colors and any text/logos, exact pose and body language]. Prioritize the exact features and details from the reference photo while applying strong South Park stylization. [OPTIONAL PROP LINE: Left hand is firmly holding [precise prop description e.g. glowing red smartphone with bright camera flash]. Right hand is holding [precise prop description].] [OPTIONAL SCENE PROP: A [prop] rests on the snow near the character's feet / leaning against the sign.] Maintain precise South Park 2D animation style, construction paper cutout aesthetic, bold black outlines, flat colors, minimal shading, simple geometric shapes, by Matt Stone and Trey Parker. **Force extremely exaggerated South Park proportions: massively oversized head (45-55% of height), very short compact torso, very short thick stubby arms and legs, almost baby-like squat stature exactly like Stan or Kyle from South Park.** Position the character standing naturally in the snow in the center or center-right foreground in front of the sign area. High detail, sharp lines, vibrant colors, no artifacts or changes to the character itself. Output exactly 2048x2048 pixels square.

Use the exact `image_id` of the character photo. Never alter the character's core appearance or gesture — only the background and add requested props.

## Group Shot Mode
When the user requests a "group shot", "all together", or similar + multiple character photos:

1. First generate clean individual portraits using Portrait Mode (recommended for maximum feature fidelity).
2. Then output a ready-to-use full scene prompt that combines them.

**Refined Group Composition Prompt Template**:

South Park 2D animation style, construction paper cutout aesthetic, bold black outlines, flat colors, minimal shading, simple geometric shapes, by Matt Stone and Trey Parker. A group of [number] distinct characters standing together in the exact clean Degen Park snowy scene with wooden "DEGEN PARK" sign on the left. [Character 1 detailed description including face, hair, clothing, accessories, pose with middle finger(s), and any props]. [Character 2 detailed description...]. [Character 3...]. **All characters use extremely exaggerated South Park proportions: massively oversized head (45-55% of height), very short compact torso, very short thick stubby arms and legs, almost baby-like squat stature exactly like Stan or Kyle from South Park.** Characters are positioned naturally side-by-side or in a small group in the foreground snow, interacting casually or posing together. High detail, sharp lines, vibrant colors, perfect composition, no overlapping or clipping. 2048x2048.

## Custom Props System
Props can be added to any portrait or group shot.

- **In hands**: Explicitly add to the prompt:  
  "Left hand is firmly holding [very specific description of prop]"  
  "Right hand is raising middle finger while holding [prop]"

- **In scene**: "A [prop description] is placed on the snow near the character's feet / leaning against the Degen Park sign."

- Always describe props with enough detail for the model to render them clearly in the cartoon style.

## Consistency Engineering & Prompt Techniques
For maximum visual consistency:

- **Character Bible**: Be extremely specific and consistent when describing features. Copy-paste the same descriptive block across prompts.
- **Style Anchor**: Always include the recommended South Park style language shown above.
- **Reference Strength**: Editing directly from the uploaded photo gives the strongest fidelity.
- **Iteration**: Generate a clean base first, then do targeted edits for props or small changes.
- **Composition Control**: Clearly state positions and framing.
- **Avoid drift**: Reference previous successful descriptions or image_ids when iterating.

## Output & Next Steps
- Clearly label each output.
- After generating, always offer logical follow-ups: add/remove props, change poses, create variations, make a group shot, try different Degen Park locations, or process new characters.

This framework now defaults to extreme Stan/Kyle-style baby-like proportions for maximum South Park authenticity while remaining flexible for custom props, poses, and different Degen Park locations. Use it on any new set of reference photos for repeatable, high-quality results.

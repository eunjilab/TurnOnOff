# -*- coding: utf-8 -*-
"""
Turn ON/OFF Brand Proposal Image Generator v2
Generates 8 images total with progress logging
"""

from google import genai
from google.genai import types
from pathlib import Path
import sys
import io
import time

# Fix encoding for Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stdout.reconfigure(line_buffering=True)

# API Setup
API_KEY = "AIzaSyD7uN5fxjKRUvQM4qQW_bI2xH2xSGn24rM"
client = genai.Client(api_key=API_KEY)

# Output directory
OUTPUT_DIR = Path("images")
OUTPUT_DIR.mkdir(exist_ok=True)

# Common style
STYLE_PREFIX = """
Style: Soft feminine aesthetic, film camera look, natural warm lighting,
pastel pink and cream tones, young Korean women in their 20s,
Brandy Melville / Miu Miu vibe, effortlessly stylish, not overly posed,
high quality fashion photography, subtle grain texture.
"""

# All 8 image prompts
IMAGE_PROMPTS = {
    # === 기존 5개 ===
    "cover": f"""
{STYLE_PREFIX}
A beautiful flat lay of minimal fashion items on cream linen fabric background.
Soft pink satin ribbon elegantly curled, a small elegant perfume bottle,
delicate gold jewelry pieces, a handwritten note card.
Elegant and simple composition with lots of negative space,
overhead shot, soft natural shadows. No text, no logos.
Horizontal 16:9 composition.
""",

    "creator": f"""
{STYLE_PREFIX}
A young Korean woman in her early 20s sitting at a bright cafe window,
writing thoughtfully in a cream colored notebook, wearing a soft cream knit sweater.
Natural golden daylight streaming in, green plants in background,
thoughtful and focused expression, candid authentic moment.
Film photography aesthetic, warm tones. Side profile or 3/4 view.
Horizontal 16:9 composition.
""",

    "onoff": f"""
{STYLE_PREFIX}
Split image composition showing clear contrast:
LEFT SIDE (OFF - casual everyday): Cozy home scene, young Korean woman in
oversized cream knit sweater and comfortable pants, relaxed on a beige sofa,
soft morning light, peaceful content expression.
RIGHT SIDE (ON - dressed up): Same style woman elegantly dressed for a date,
wearing a soft pink feminine dress, subtle makeup, confident smile,
warm evening restaurant ambiance with soft lighting.
Clear visual contrast between casual home comfort and dressed-up elegance.
Horizontal 16:9 composition.
""",

    "target": f"""
{STYLE_PREFIX}
Three young Korean women in their early 20s walking together on a charming street,
spring cherry blossom atmosphere with soft pink petals,
laughing naturally and joyfully together as close friends.
Wearing beautifully coordinated outfits in soft pink, cream, and white tones.
Best friends vibe, candid joyful moment, golden hour warm lighting.
Fashion editorial feel but natural and authentic.
Horizontal 16:9 composition.
""",

    "vision": f"""
{STYLE_PREFIX}
Abstract soft aesthetic background perfect for text overlay.
Beautiful soft gradient blending cream, blush pink, and warm beige colors.
Subtle dreamy bokeh lights effect creating depth.
Ethereal, minimal, elegant design. Plenty of negative space for text placement.
No objects, no people, just beautiful soft abstract background.
Horizontal 16:9 composition.
""",

    # === 추가 3개 ===
    "plan": f"""
{STYLE_PREFIX}
A clean, minimal workspace flatlay on white marble surface.
Rose gold laptop partially visible, a small notebook with cream pages,
a cup of latte with heart art, fresh pink peonies in a small vase,
gold pen, soft morning light from window.
Business meets feminine aesthetic, organized and aspirational.
Overhead shot, soft shadows, no text visible.
Horizontal 16:9 composition.
""",

    "request": f"""
{STYLE_PREFIX}
Abstract tech-meets-soft aesthetic image.
Soft pink and cream gradient background with subtle geometric shapes,
floating translucent spheres and soft light flares,
modern and innovative feeling but still feminine and warm.
Perfect for AI/technology related content while maintaining soft brand aesthetic.
Dreamy, ethereal, slightly futuristic but approachable.
Horizontal 16:9 composition.
""",

    "ending": f"""
{STYLE_PREFIX}
Elegant and hopeful closing image.
Soft pink sunrise or sunset sky with gentle clouds,
warm golden light rays streaming through,
dreamy and aspirational atmosphere.
Feeling of new beginnings, hope, and beautiful possibilities.
Peaceful, serene, emotionally uplifting.
No people, just beautiful sky and light.
Horizontal 16:9 composition.
"""
}


def log(msg):
    """Print with timestamp"""
    timestamp = time.strftime("%H:%M:%S")
    print(f"[{timestamp}] {msg}", flush=True)


def generate_and_save_image(name: str, prompt: str, index: int, total: int):
    """Generate image with Gemini and save"""
    log(f"({index}/{total}) Generating '{name}'...")

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash-exp",
            contents=[prompt],
            config=types.GenerateContentConfig(
                response_modalities=['TEXT', 'IMAGE']
            )
        )

        output_path = OUTPUT_DIR / f"{name}.png"

        for part in response.candidates[0].content.parts:
            if part.inline_data is not None:
                image_data = part.inline_data.data
                with open(output_path, 'wb') as f:
                    f.write(image_data)
                log(f"    OK - Saved: {name}.png")
                return True
            elif part.text is not None:
                log(f"    Info: {part.text[:80]}...")

        log(f"    FAIL - No image generated")
        return False

    except Exception as e:
        log(f"    ERROR - {e}")
        return False


def main():
    log("=" * 50)
    log("Turn ON/OFF Brand Image Generation v2")
    log(f"Total images to generate: {len(IMAGE_PROMPTS)}")
    log("=" * 50)

    success_count = 0
    total = len(IMAGE_PROMPTS)

    for i, (name, prompt) in enumerate(IMAGE_PROMPTS.items(), 1):
        if generate_and_save_image(name, prompt, i, total):
            success_count += 1
        time.sleep(1)  # Rate limiting

    log("")
    log("=" * 50)
    log(f"COMPLETE! {success_count}/{total} images generated")
    log(f"Output folder: {OUTPUT_DIR.absolute()}")
    log("=" * 50)

    # Summary
    log("")
    log("Generated images:")
    for name in IMAGE_PROMPTS.keys():
        path = OUTPUT_DIR / f"{name}.png"
        status = "OK" if path.exists() else "MISSING"
        log(f"  - {name}.png [{status}]")


if __name__ == "__main__":
    main()

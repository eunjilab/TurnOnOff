# -*- coding: utf-8 -*-
"""
Turn ON/OFF Brand Proposal Image Generator
Using Gemini API to create consistent style images
"""

from google import genai
from google.genai import types
from pathlib import Path
import sys
import io

# Fix encoding for Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# API Setup
API_KEY = "AIzaSyD7uN5fxjKRUvQM4qQW_bI2xH2xSGn24rM"
client = genai.Client(api_key=API_KEY)

# Output directory
OUTPUT_DIR = Path("images")
OUTPUT_DIR.mkdir(exist_ok=True)

# Common style (Brandy Melville / Miu Miu vibe, young feminine)
STYLE_PREFIX = """
Style: Soft feminine aesthetic, film camera look, natural warm lighting,
pastel pink and cream tones, young Korean women in their 20s,
Brandy Melville / Miu Miu vibe, effortlessly stylish, not overly posed,
high quality fashion photography, subtle grain texture.
"""

# Image prompts for each slide
IMAGE_PROMPTS = {
    "cover": f"""
{STYLE_PREFIX}
A beautiful flat lay of minimal fashion items on cream fabric background.
Soft pink ribbon, a small perfume bottle, delicate gold jewelry,
a handwritten note card. Elegant and simple, negative space,
overhead shot, soft natural shadows. No text, no logos.
Horizontal 16:9 composition.
""",

    "creator": f"""
{STYLE_PREFIX}
A young Korean woman in her early 20s sitting at a bright cafe window,
writing in a notebook, wearing a soft cream knit sweater.
Natural daylight streaming in, plants in background,
thoughtful and focused expression, candid moment.
Film photography aesthetic, warm tones. Side profile or 3/4 view.
Horizontal 16:9 composition.
""",

    "onoff": f"""
{STYLE_PREFIX}
Split image composition showing contrast:
LEFT SIDE (OFF - casual): Cozy home scene, oversized cream sweater, comfortable,
relaxed on a sofa, soft morning light, peaceful.
RIGHT SIDE (ON - dressed up): Same style woman dressed for a date, soft pink dress,
light makeup, confident, evening ambiance.
Clear visual contrast between casual and dressed-up looks.
Horizontal 16:9 composition.
""",

    "target": f"""
{STYLE_PREFIX}
Three young Korean women in their early 20s walking together on a pretty street,
spring atmosphere with soft colors, laughing naturally together.
Wearing coordinated outfits in soft pink, cream, and white tones.
Best friends vibe, candid joyful moment, golden hour lighting.
Fashion editorial feel but natural.
Horizontal 16:9 composition.
""",

    "vision": f"""
{STYLE_PREFIX}
Abstract soft aesthetic background suitable for text overlay.
Soft gradient of cream, blush pink, and warm beige colors.
Subtle fabric texture or soft bokeh lights effect.
Dreamy, ethereal, minimal design. Good negative space for text.
No objects, no people, just beautiful soft background.
Horizontal 16:9 composition.
"""
}


def generate_and_save_image(name: str, prompt: str):
    """Generate image with Gemini and save"""
    print(f"\n[*] Generating '{name}' image...")

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash-exp",
            contents=[prompt],
            config=types.GenerateContentConfig(
                response_modalities=['TEXT', 'IMAGE']
            )
        )

        # Save image
        output_path = OUTPUT_DIR / f"{name}.png"

        for part in response.candidates[0].content.parts:
            if part.inline_data is not None:
                # Save image data
                image_data = part.inline_data.data
                with open(output_path, 'wb') as f:
                    f.write(image_data)
                print(f"    [OK] Saved: {output_path}")
                return True
            elif part.text is not None:
                print(f"    [INFO] {part.text[:100]}...")

        print(f"    [FAIL] No image in response")
        return False

    except Exception as e:
        print(f"    [ERROR] {e}")
        return False


def main():
    print("=" * 50)
    print("Turn ON/OFF Brand Image Generation")
    print("=" * 50)

    success_count = 0
    for name, prompt in IMAGE_PROMPTS.items():
        if generate_and_save_image(name, prompt):
            success_count += 1

    print("\n" + "=" * 50)
    print(f"Done! {success_count}/{len(IMAGE_PROMPTS)} images generated")
    print(f"Output: {OUTPUT_DIR.absolute()}")
    print("=" * 50)


if __name__ == "__main__":
    main()

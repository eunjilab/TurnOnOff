# -*- coding: utf-8 -*-
"""
Turn ON/OFF Brand Proposal Image Generator v3
Using Nano Banana (gemini-2.5-flash-image) for better quality
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

# Common style - more specific and refined
STYLE_PREFIX = """
High-end fashion editorial photography style.
Shot on film camera with natural warm golden hour lighting.
Soft pastel color palette: blush pink, cream, warm beige, soft white.
Young Korean women in their 20s, natural beauty, minimal makeup.
Brandy Melville and Miu Miu aesthetic - effortlessly chic, not overdone.
Subtle film grain texture, dreamy bokeh, magazine quality.
NO AI-generated look, NO plastic skin, NO overly saturated colors.
"""

# Images to regenerate + new ones
IMAGE_PROMPTS = {
    # 02-1 타겟고객 - 더 자연스럽게
    "target": f"""
{STYLE_PREFIX}
Candid photo of three young Korean women best friends in their early 20s.
Walking casually on a beautiful tree-lined street during golden hour.
Wearing coordinated feminine outfits: soft pink cardigan, cream knit, white blouse.
Natural laughing moment, genuine friendship vibes.
Shot from a slight distance, environmental portrait style.
Spring or autumn atmosphere, soft natural backlight.
Horizontal 16:9 composition.
""",

    # 03 실행계획 - 모던하고 미니멀하게
    "plan": f"""
{STYLE_PREFIX}
Minimal aesthetic workspace flatlay on clean white marble.
Items arranged with lots of negative space:
- Small bouquet of soft pink roses in simple glass vase
- One elegant gold pen
- Cream colored linen notebook (closed)
- Single cup of oat latte
Soft morning window light creating gentle shadows.
Clean, organized, aspirational but not cluttered.
Modern feminine entrepreneur aesthetic.
Overhead shot, horizontal 16:9 composition.
""",

    # 06 요청사항 - 브랜드 무드에 맞게 따뜻하게
    "request": f"""
{STYLE_PREFIX}
Soft abstract background with warm feminine tones.
Gentle gradient from cream to soft blush pink.
Subtle texture like soft linen or silk fabric.
Delicate light flares and soft bokeh circles.
Dreamy, ethereal, elegant atmosphere.
Perfect for text overlay with good negative space.
Warm and inviting, not cold or techy.
NO geometric shapes, NO hard edges.
Horizontal 16:9 composition.
""",

    # 05 목표 및 제안 - 새로 추가
    "goal": f"""
{STYLE_PREFIX}
Inspirational lifestyle photo.
Young Korean woman in her 20s looking out a large window.
Wearing soft cream sweater, holding a warm cup of coffee.
Soft morning light streaming in, creating beautiful rim light.
Thoughtful, hopeful expression, looking toward the future.
Cozy interior with plants, soft furnishings in background.
Feeling of new beginnings and possibilities.
Horizontal 16:9 composition.
""",

    # 07 기대효과 - 새로 추가
    "summary": f"""
{STYLE_PREFIX}
Beautiful soft gradient sky at golden hour.
Blend of soft pink, peach, cream, and warm gold tones.
Gentle clouds with soft edges.
Feeling of hope, success, and beautiful possibilities.
Dreamy and ethereal atmosphere.
Perfect as background for text overlay.
NO sun directly visible, just soft diffused light.
Horizontal 16:9 composition.
"""
}


def log(msg):
    """Print with timestamp"""
    timestamp = time.strftime("%H:%M:%S")
    print(f"[{timestamp}] {msg}", flush=True)


def generate_and_save_image(name: str, prompt: str, index: int, total: int):
    """Generate image with Gemini Nano Banana and save"""
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
    log("Turn ON/OFF Image Generation v3")
    log("Regenerating: target, plan, request")
    log("Adding new: goal, summary")
    log(f"Total: {len(IMAGE_PROMPTS)} images")
    log("=" * 50)

    success_count = 0
    total = len(IMAGE_PROMPTS)

    for i, (name, prompt) in enumerate(IMAGE_PROMPTS.items(), 1):
        if generate_and_save_image(name, prompt, i, total):
            success_count += 1
        time.sleep(1)

    log("")
    log("=" * 50)
    log(f"COMPLETE! {success_count}/{total} images generated")
    log("=" * 50)

    log("")
    log("Generated images:")
    for name in IMAGE_PROMPTS.keys():
        path = OUTPUT_DIR / f"{name}.png"
        status = "OK" if path.exists() else "MISSING"
        log(f"  - {name}.png [{status}]")


if __name__ == "__main__":
    main()

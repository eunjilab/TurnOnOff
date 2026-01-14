# -*- coding: utf-8 -*-
"""
Turn ON/OFF Brand Image Generator
Using REAL Nano Banana (gemini-2.5-flash-image)
"""

from google import genai
from pathlib import Path
import sys
import io
import time

# Fix encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stdout.reconfigure(line_buffering=True)

# API Setup
API_KEY = "AIzaSyD7uN5fxjKRUvQM4qQW_bI2xH2xSGn24rM"
client = genai.Client(api_key=API_KEY)

OUTPUT_DIR = Path("images")
OUTPUT_DIR.mkdir(exist_ok=True)

# High quality prompts
STYLE = """
High-end Korean fashion editorial, shot on 35mm film.
Soft pastel tones: blush pink, cream, warm beige.
Natural golden hour lighting, subtle film grain.
Brandy Melville / Miu Miu aesthetic.
Magazine quality, NOT AI-looking.
"""

PROMPTS = {
    "target": f"""{STYLE}
Three young Korean women friends walking on tree-lined street.
Coordinated outfits in pink, cream, white. Candid laughing moment.
Golden hour backlight, environmental portrait. 16:9 horizontal.""",

    "plan": f"""{STYLE}
Minimal workspace flatlay on white marble.
Pink roses in glass vase, gold pen, cream notebook, latte.
Morning window light, clean negative space. 16:9 horizontal.""",

    "request": f"""{STYLE}
Soft abstract background. Cream to blush pink gradient.
Subtle linen texture, dreamy bokeh lights.
Warm and elegant, good for text overlay. 16:9 horizontal.""",

    "goal": f"""{STYLE}
Young Korean woman by large window, holding coffee.
Cream sweater, thoughtful hopeful expression.
Morning light, cozy interior with plants. 16:9 horizontal.""",

    "summary": f"""{STYLE}
Golden hour sky, soft pink and peach clouds.
Dreamy ethereal atmosphere, feeling of hope.
Perfect background for text. 16:9 horizontal."""
}


def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


def generate(name, prompt, i, total):
    log(f"({i}/{total}) Generating '{name}'...")
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash-image",  # NANO BANANA!
            contents=[prompt],
        )

        path = OUTPUT_DIR / f"{name}.png"
        for part in response.parts:
            if part.inline_data is not None:
                image = part.as_image()
                image.save(str(path))
                log(f"    OK - {name}.png")
                return True
            elif part.text:
                log(f"    Info: {part.text[:60]}...")

        log(f"    FAIL - No image")
        return False
    except Exception as e:
        log(f"    ERROR - {e}")
        return False


def main():
    log("=" * 50)
    log("NANO BANANA (gemini-2.5-flash-image)")
    log(f"Generating {len(PROMPTS)} images")
    log("=" * 50)

    ok = 0
    for i, (name, prompt) in enumerate(PROMPTS.items(), 1):
        if generate(name, prompt, i, len(PROMPTS)):
            ok += 1
        time.sleep(1)

    log("")
    log("=" * 50)
    log(f"DONE! {ok}/{len(PROMPTS)} images")
    log("=" * 50)


if __name__ == "__main__":
    main()

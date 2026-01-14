# -*- coding: utf-8 -*-
"""
Regenerate cover, creator, onoff with Nano Banana
"""

from google import genai
from pathlib import Path
import sys
import io
import time

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stdout.reconfigure(line_buffering=True)

API_KEY = "AIzaSyD7uN5fxjKRUvQM4qQW_bI2xH2xSGn24rM"
client = genai.Client(api_key=API_KEY)

OUTPUT_DIR = Path("images")

STYLE = """
High-end Korean fashion editorial, Vogue Korea style.
Shot on Contax T2 film camera, 35mm.
Soft pastel tones: dusty pink, warm cream, soft beige.
Natural golden hour or soft window light.
Miu Miu / Brandy Melville / gentle feminine aesthetic.
Magazine quality, elegant, NOT cheesy or AI-looking.
"""

PROMPTS = {
    # 표지 - 세련된 플랫레이
    "cover": f"""{STYLE}
Elegant minimal flatlay on cream linen fabric.
Delicate items: silk ribbon in dusty rose, vintage perfume bottle,
single dried flower stem, handwritten letter on textured paper,
small gold earring. Soft natural shadows from window light.
Lots of breathing space, editorial composition.
NO clutter, very minimal and refined. 16:9 horizontal.""",

    # 01 브랜드 생각 - 카페에서 작업하는 여성
    "creator": f"""{STYLE}
Young Korean woman in her 20s at minimalist cafe.
Wearing cream cashmere sweater, writing in leather journal.
Soft side profile, natural window light on her face.
Warm latte beside her, green plants softly blurred in background.
Thoughtful creative moment, genuine and unstaged feeling.
Film photography aesthetic with subtle grain. 16:9 horizontal.""",

    # 02 ON/OFF - 확실한 대비
    "onoff": f"""{STYLE}
Elegant diptych showing same young Korean woman in two moods:
LEFT: Cozy morning at home, oversized cream knit sweater,
messy bun, holding warm mug, soft morning window light, relaxed smile.
RIGHT: Evening date look, elegant dusty pink slip dress,
soft waves hair, delicate jewelry, warm restaurant ambiance, confident.
Clear contrast between casual comfort and dressed-up elegance.
Both sides equally beautiful, just different vibes. 16:9 horizontal.""",

    # request - 추상 배경으로 다시
    "request": f"""
Soft dreamy abstract background for text overlay.
Gentle gradient from warm cream to dusty blush pink.
Subtle texture like soft watercolor wash or silk fabric.
Delicate bokeh light circles floating softly.
Ethereal, minimal, elegant. NO people, NO objects.
Just beautiful soft colors and light. 16:9 horizontal.""",

    # summary - 하늘 배경으로 다시
    "summary": f"""
Dreamy golden hour sky photograph.
Soft gradient of dusty pink, peach, cream, pale gold.
Gentle wispy clouds with soft edges.
Feeling of hope, new beginnings, possibilities.
Ethereal and peaceful atmosphere.
NO people, just beautiful sky. 16:9 horizontal."""
}


def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


def generate(name, prompt, i, total):
    log(f"({i}/{total}) Generating '{name}'...")
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash-image",
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

        log(f"    FAIL")
        return False
    except Exception as e:
        log(f"    ERROR - {e}")
        return False


def main():
    log("=" * 50)
    log("NANO BANANA - Regenerating 1,2,3 + request,summary")
    log(f"Total: {len(PROMPTS)} images")
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

# -*- coding: utf-8 -*-
"""
Regenerate bland background images with Nano Banana
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
    # plan - 더 임팩트 있게
    "plan": f"""{STYLE}
Elegant flatlay on marble surface showing a mood board.
Polaroid photos scattered, fabric swatches in dusty pink and cream,
a vintage brass clip, dried eucalyptus sprig, handwritten notes.
Soft natural shadows, editorial styling.
Breathing space, minimal but curated. 16:9 horizontal.""",

    # vision - 추상 말고 실제 장면
    "vision": f"""{STYLE}
Behind the scenes of a fashion photoshoot.
Soft focus on clothing rack with dusty pink and cream garments,
warm afternoon light streaming through sheer curtains.
A mirror reflecting soft bokeh, intimate creative atmosphere.
Dreamy, aspirational, magazine editorial vibe. 16:9 horizontal.""",

    # request - 오브젝트 플랫레이
    "request": f"""{STYLE}
Minimal flatlay on cream linen.
A single vintage brass key, a wax seal stamp,
a piece of handmade paper with soft torn edges,
a delicate dried flower petal.
Soft morning light, gentle shadows.
Clean, elegant, symbolic of partnership. 16:9 horizontal.""",

    # summary - 의미있는 장면
    "summary": f"""{STYLE}
Hands holding a beautifully wrapped gift box in dusty pink paper.
Cream ribbon, soft natural light from window.
Warm intimate moment, giving/receiving symbolism.
Soft focus background, elegant feminine aesthetic. 16:9 horizontal.""",

    # ending - 감사의 의미
    "ending": f"""{STYLE}
Close-up of a handwritten thank you card on textured cream paper.
A single fresh pink rose laying beside it.
Vintage gold pen nearby.
Soft natural light, warm tones.
Intimate, personal, heartfelt. 16:9 horizontal."""
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
    log("NANO BANANA - Regenerating background images")
    log(f"Images: plan, vision, request, summary, ending")
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

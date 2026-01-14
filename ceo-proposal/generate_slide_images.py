# -*- coding: utf-8 -*-
"""
Generate images for slides 03, 04, 05
"""

from google import genai
from pathlib import Path
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stdout.reconfigure(line_buffering=True)

API_KEY = "AIzaSyD7uN5fxjKRUvQM4qQW_bI2xH2xSGn24rM"
client = genai.Client(api_key=API_KEY)

OUTPUT_DIR = Path("images")

# 03. 실행 계획 - 계획 세우는 모습
PROMPT_PLAN = """
High-end Korean fashion editorial, Vogue Korea style.
Shot on Contax T2 film camera, 35mm.

Young Korean woman in her 20s working on her laptop in a cozy cafe or workspace.
She's planning, thinking, looking focused but calm.
Wearing soft cream knit sweater, Brandy Melville aesthetic.
Soft natural window light, warm golden hour tones.
Dusty pink, warm cream, soft beige color palette.
Magazine quality, elegant, NOT cheesy or AI-looking.
16:9 horizontal composition.
"""

# 04. 준비 상황 - 학습하는 모습
PROMPT_STUDY = """
High-end Korean fashion editorial, Vogue Korea style.
Shot on Contax T2 film camera, 35mm.

Close-up of elegant feminine hands writing notes in a beautiful notebook.
Soft pink pen, delicate accessories on wrist.
Coffee cup nearby, warm cafe atmosphere.
Soft natural light, cozy studying mood.
Dusty pink, warm cream, soft beige color palette.
Magazine quality, elegant, NOT cheesy or AI-looking.
16:9 horizontal composition.
"""

# 05. 요청 배경 - 파트너십/함께 성장
PROMPT_PARTNER = """
High-end Korean fashion editorial, Vogue Korea style.
Shot on Contax T2 film camera, 35mm.

Two young Korean women walking together, shot from behind.
One in cream knit, one in dusty pink blouse.
Walking towards soft golden light, suggesting future together.
Friendship, partnership, trust vibe.
Soft pastel tones: dusty pink, warm cream, soft beige.
Natural golden hour light.
Magazine quality, elegant, NOT cheesy or AI-looking.
16:9 horizontal composition.
"""

images_to_generate = [
    ("slide03_plan.png", PROMPT_PLAN, "03. 실행 계획"),
    ("slide04_study.png", PROMPT_STUDY, "04. 준비 상황"),
    ("slide05_partner.png", PROMPT_PARTNER, "05. 요청 배경"),
]

for filename, prompt, slide_name in images_to_generate:
    print(f"\n생성 중: {slide_name}...")
    try:
        response = client.models.generate_content(
            model="gemini-3-pro-image-preview",
            contents=[prompt],
        )

        for part in response.parts:
            if part.inline_data is not None:
                image = part.as_image()
                image.save(str(OUTPUT_DIR / filename))
                print(f"SUCCESS - {filename} saved!")
            elif part.text:
                print(f"Info: {part.text[:80]}...")

    except Exception as e:
        print(f"ERROR: {e}")

print("\n모든 이미지 생성 완료!")

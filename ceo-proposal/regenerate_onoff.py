# -*- coding: utf-8 -*-
"""
Regenerate onoff.png with lovely/Brandy Melville/Miu Miu style
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

PROMPT = """
Fashion photo, split screen, same Korean girl.

LEFT (OFF):
Sky blue oversized fuzzy knit cardigan.
Gray leggings or skinny pants.
Brown baseball cap.
Brown leather loafers.
Brown leather tote bag.
Sitting on stone steps, casual pose.
Street style, natural daylight.

RIGHT (ON):
Cream knit peplum cardigan with buttons.
Cream knit mini skirt set.
Burgundy beret hat.
Burgundy small handbag.
Burgundy knee high boots.
Gold hoop earrings (no pearls).
Feminine lovely but not formal.
Standing pose, gray background.

Korean woman, 20s, long black hair, pretty face.
Magazine editorial photo quality.
16:9 horizontal split.
"""

print("Generating new onoff.png with lovely style...")

try:
    response = client.models.generate_content(
        model="gemini-2.5-flash-image",
        contents=[PROMPT],
    )

    for part in response.parts:
        if part.inline_data is not None:
            image = part.as_image()
            image.save(str(OUTPUT_DIR / "onoff.png"))
            print("SUCCESS - onoff.png saved!")
        elif part.text:
            print(f"Info: {part.text[:100]}...")

except Exception as e:
    print(f"ERROR: {e}")

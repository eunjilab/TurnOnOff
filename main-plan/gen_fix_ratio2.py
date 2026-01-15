# -*- coding: utf-8 -*-
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from google import genai
from google.genai import types
import time

API_KEY = "AIzaSyD7uN5fxjKRUvQM4qQW_bI2xH2xSGn24rM"
client = genai.Client(api_key=API_KEY)

images = [
    {
        "filename": "why_business_wide.png",
        "prompt": "Fashion business idea concept, light bulb with dress inside, soft pastel pink background, clean minimalist illustration, centered composition, NO text"
    },
    {
        "filename": "investment_wide.png",
        "prompt": "Business growth investment concept, arrow going up with coins and bar chart, soft pastel pink cream gold colors, clean minimalist infographic, centered, NO text"
    },
    {
        "filename": "revenue_chart_wide.png",
        "prompt": "Simple revenue growth bar chart with upward trend arrow, soft pastel pink gradient bars, clean minimalist style, centered, NO text NO labels"
    },
    {
        "filename": "legal_wide.png",
        "prompt": "Business legal documents on elegant desk, contract papers pen stamp neatly arranged, soft pastel pink cream aesthetic, clean professional style, centered, NO text"
    }
]

for i, img in enumerate(images):
    print(f"\n[{i+1}/{len(images)}] Generating {img['filename']}...")

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash-image",
            contents=[img['prompt']],
            config=types.GenerateContentConfig(
                response_modalities=['image', 'text'],
                image_config=types.ImageConfig(
                    aspect_ratio="16:9"
                )
            )
        )

        for part in response.parts:
            if part.inline_data is not None:
                image = part.as_image()
                image.save(f"images/{img['filename']}")
                print(f"Saved: images/{img['filename']}")
                from PIL import Image
                saved_img = Image.open(f"images/{img['filename']}")
                w, h = saved_img.size
                print(f"Size: {w}x{h}, Ratio: {w/h:.2f}")
                break
        else:
            print("No image generated")
    except Exception as e:
        print(f"Error: {e}")

    time.sleep(2)

print("\nDone!")

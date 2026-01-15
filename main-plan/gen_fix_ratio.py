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
        "prompt": """
Fashion business idea concept, light bulb with dress and fashion elements inside.
Soft pastel pink gradient background.
Clean minimalist illustration style.
Main element centered horizontally.
NO text.
16:9 wide horizontal aspect ratio.
"""
    },
    {
        "filename": "investment_wide.png",
        "prompt": """
Business investment growth concept infographic.
Arrow going up with coins and bar chart.
Soft pastel pink, cream, gold colors.
Clean minimalist style, elements centered.
NO text.
16:9 wide horizontal aspect ratio.
"""
    },
    {
        "filename": "revenue_chart_wide.png",
        "prompt": """
Simple revenue growth bar chart with upward arrow.
Soft pastel pink gradient bars.
Clean minimalist infographic style.
Chart centered in composition.
NO text, NO labels.
16:9 wide horizontal aspect ratio.
"""
    },
    {
        "filename": "legal_wide.png",
        "prompt": """
Business legal documents on elegant desk.
Contract papers, pen, stamp, organized neatly.
Soft pastel pink and cream aesthetic.
Clean professional minimalist style.
Elements centered in frame.
NO text.
16:9 wide horizontal aspect ratio.
"""
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
            )
        )

        for part in response.parts:
            if part.inline_data is not None:
                image = part.as_image()
                image.save(f"images/{img['filename']}")
                print(f"Saved: images/{img['filename']}")
                # Check size
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

print("\n" + "="*50)
print("Done!")

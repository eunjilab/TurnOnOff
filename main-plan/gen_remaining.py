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
        "filename": "style_guide.png",
        "prompt": "Fashion style guide moodboard, color palette swatches, fabric textures, outfit combinations, soft pastel pink cream beige aesthetic, clean minimalist layout, centered composition, NO text"
    },
    {
        "filename": "growth_roadmap.png",
        "prompt": "Business growth roadmap timeline infographic, steps going upward, milestones marked, soft pastel pink cream colors, clean minimalist style, centered horizontal layout, NO text NO labels"
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

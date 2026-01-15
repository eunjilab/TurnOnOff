# -*- coding: utf-8 -*-
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from google import genai
from google.genai import types
import time

API_KEY = "AIzaSyD7uN5fxjKRUvQM4qQW_bI2xH2xSGn24rM"
client = genai.Client(api_key=API_KEY)

images_to_generate = [
    {
        "filename": "why_business.png",
        "prompt": """
Fashion business startup concept illustration.
Light bulb with fashion elements inside.
Soft pastel pink, cream, beige colors.
Minimalist, clean, modern style.
NO text, elegant aesthetic.
16:9 horizontal composition.
"""
    },
    {
        "filename": "market_problem.png",
        "prompt": """
Fashion shopping frustration concept.
Woman confused with too many clothing options.
Soft pastel colors: dusty pink, cream.
Minimalist illustration style.
NO text, clean aesthetic.
16:9 horizontal composition.
"""
    },
    {
        "filename": "set_strategy.png",
        "prompt": """
Fashion outfit set coordination flat lay.
Complete outfit laid out beautifully: top, bottom, accessories.
Soft pastel pink, cream, beige tones.
Clean, organized, magazine style.
NO text, elegant aesthetic.
16:9 horizontal composition.
"""
    },
    {
        "filename": "investment.png",
        "prompt": """
Business investment and growth concept.
Minimalist illustration of funding and scaling.
Soft pastel colors: dusty pink, gold accents, cream.
Clean, professional, modern style.
NO text, elegant aesthetic.
16:9 horizontal composition.
"""
    },
    {
        "filename": "revenue_chart.png",
        "prompt": """
Business revenue growth chart illustration.
Simple bar chart or line graph going upward.
Soft pastel pink and cream colors.
Clean, minimalist infographic style.
NO text labels, elegant aesthetic.
16:9 horizontal composition.
"""
    },
    {
        "filename": "team.png",
        "prompt": """
Small startup team working together.
Fashion brand creative workspace.
Soft pastel pink and cream aesthetic.
Clean, modern, collaborative atmosphere.
NO text, magazine style photography.
16:9 horizontal composition.
"""
    },
    {
        "filename": "legal.png",
        "prompt": """
Business legal documents and compliance concept.
Elegant desk with documents, pen, stamp.
Soft pastel pink, cream, beige tones.
Clean, professional, minimalist style.
NO text, sophisticated aesthetic.
16:9 horizontal composition.
"""
    }
]

for i, img in enumerate(images_to_generate):
    print(f"\n[{i+1}/{len(images_to_generate)}] Generating {img['filename']}...")

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
                break
        else:
            print(f"No image generated for {img['filename']}")

    except Exception as e:
        print(f"Error: {e}")

    time.sleep(2)  # Rate limit

print("\n" + "="*50)
print("All done!")

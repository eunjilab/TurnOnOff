# -*- coding: utf-8 -*-
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from google import genai
from google.genai import types

API_KEY = "AIzaSyD7uN5fxjKRUvQM4qQW_bI2xH2xSGn24rM"
client = genai.Client(api_key=API_KEY)

prompt = """
Young Korean women in their early 20s, university students.
Casual trendy fashion, Y2K style.
Group of friends taking selfie or having fun.
Soft pastel pink, cream aesthetic.
Youthful, fresh, energetic vibe.
NOT corporate, NOT office workers.
College campus or cafe atmosphere.
NO text, magazine style photography.
16:9 horizontal composition.
"""

print("Generating target_customer_new.png...")

response = client.models.generate_content(
    model="gemini-2.5-flash-image",
    contents=[prompt],
    config=types.GenerateContentConfig(
        response_modalities=['image', 'text'],
    )
)

for part in response.parts:
    if part.inline_data is not None:
        image = part.as_image()
        image.save("images/target_customer_new.png")
        print("Saved: images/target_customer_new.png")
        break
else:
    print("No image generated")

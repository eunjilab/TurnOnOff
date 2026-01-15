# -*- coding: utf-8 -*-
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from google import genai
from google.genai import types

API_KEY = "AIzaSyD7uN5fxjKRUvQM4qQW_bI2xH2xSGn24rM"
client = genai.Client(api_key=API_KEY)

prompt = """
Instagram feed mockup for fashion brand.
Multiple phone screens showing fashion content grid.
Soft pink and white aesthetic.
Floating smartphones on pastel gradient background.
Fashion reels and outfit photos visible on screens.
NO text, clean UI design.
16:9 horizontal composition.
High quality 3D render style, professional.
"""

print("Generating sns_mockup.png...")

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
        image.save("images/sns_mockup.png")
        print("Saved: images/sns_mockup.png")
        break
else:
    print("No image generated")

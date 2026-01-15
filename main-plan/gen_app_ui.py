# -*- coding: utf-8 -*-
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from google import genai
from google.genai import types

API_KEY = "AIzaSyD7uN5fxjKRUvQM4qQW_bI2xH2xSGn24rM"
client = genai.Client(api_key=API_KEY)

prompt = """
Fashion app UI design mockup.
Multiple app screens showing different features.
Home feed, AI chat, outfit upload screens.
Soft pink and white color scheme.
Clean modern UI design.
Floating phone mockups on gradient background.
NO text labels, clean interface.
16:9 horizontal composition.
High quality 3D render style.
"""

print("Generating app_features.png...")

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
        image.save("images/app_features.png")
        print("Saved: images/app_features.png")
        break
else:
    print("No image generated")

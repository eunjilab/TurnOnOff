# -*- coding: utf-8 -*-
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from google import genai
from google.genai import types
import os

API_KEY = "AIzaSyD7uN5fxjKRUvQM4qQW_bI2xH2xSGn24rM"
client = genai.Client(api_key=API_KEY)

prompt = """
Minimalist world map infographic style.
Soft pastel colors: dusty pink, cream, beige.
Clean, modern, professional business presentation style.
Highlighting Asia, USA, Europe regions with subtle glow.
NO text, NO labels, NO country names.
Fashion brand global expansion concept.
16:9 horizontal composition.
High quality, elegant, NOT cheesy.
"""

print("Generating global_expansion.png...")

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
        image.save("images/global_expansion.png")
        print("Saved: images/global_expansion.png")
        break
else:
    print("No image generated")

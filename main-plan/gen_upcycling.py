# -*- coding: utf-8 -*-
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from google import genai
from google.genai import types

API_KEY = "AIzaSyD7uN5fxjKRUvQM4qQW_bI2xH2xSGn24rM"
client = genai.Client(api_key=API_KEY)

prompt = """
Sustainable fashion upcycling concept.
Before and after transformation of clothing.
Soft pastel colors: dusty pink, cream, beige, sage green.
Clean, modern, eco-friendly aesthetic.
Fabric scraps being transformed into beautiful garments.
NO text, NO labels.
Fashion atelier workshop atmosphere.
16:9 horizontal composition.
High quality, elegant, magazine style.
"""

print("Generating upcycling.png...")

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
        image.save("images/upcycling.png")
        print("Saved: images/upcycling.png")
        break
else:
    print("No image generated")

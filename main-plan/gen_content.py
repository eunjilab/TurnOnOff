# -*- coding: utf-8 -*-
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from google import genai
from google.genai import types

API_KEY = "AIzaSyD7uN5fxjKRUvQM4qQW_bI2xH2xSGn24rM"
client = genai.Client(api_key=API_KEY)

prompt = """
Fashion vlog content creation scene.
Young woman filming fashion content with camera and ring light.
Soft pastel pink and cream aesthetic.
Behind the scenes of fashion brand storytelling.
Clean, bright, modern workspace.
NO text, editorial style.
16:9 horizontal composition.
High quality, magazine style photography.
"""

print("Generating content_story.png...")

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
        image.save("images/content_story.png")
        print("Saved: images/content_story.png")
        break
else:
    print("No image generated")

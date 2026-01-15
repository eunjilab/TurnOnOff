# -*- coding: utf-8 -*-
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from google import genai
from google.genai import types
from PIL import Image
import os

API_KEY = "AIzaSyD7uN5fxjKRUvQM4qQW_bI2xH2xSGn24rM"
client = genai.Client(api_key=API_KEY)

def generate_image(prompt, filename, aspect_ratio="16:9"):
    print(f"Generating: {filename}")
    print(f"Prompt: {prompt[:50]}...")

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
            image.save(f"images/{filename}")
            print(f"Saved: images/{filename}")
            return True

    print("No image generated")
    return False

# 1. Positioning Mood - More elegant
positioning_prompt = """
High-end fashion brand mood board, editorial style.
Soft feminine aesthetic with dusty pink, warm cream, beige tones.
NO TEXT, NO WORDS, NO LETTERS.
Elegant fabric textures, soft silk, delicate details.
Sophisticated Korean fashion brand identity.
Minimalist, clean, luxurious feel.
Magazine quality, NOT cheesy or AI-looking.
16:9 horizontal composition.
"""

# 2. App Vision - Fashion app concept
app_vision_prompt = """
Modern fashion app interface mockup on smartphone.
Clean UI design showing outfit grid layout.
Soft pink and white color scheme.
Floating phone design on gradient background.
Professional app store screenshot style.
NO text on the image.
16:9 horizontal composition.
High quality 3D render style.
"""

if __name__ == "__main__":
    os.makedirs("images", exist_ok=True)

    print("=" * 50)
    print("1. Regenerating positioning_mood.png")
    print("=" * 50)
    generate_image(positioning_prompt, "positioning_mood_new.png")

    print("\n" + "=" * 50)
    print("2. Regenerating app_vision.png")
    print("=" * 50)
    generate_image(app_vision_prompt, "app_vision_new.png")

    print("\nDone!")

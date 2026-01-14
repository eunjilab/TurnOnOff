# -*- coding: utf-8 -*-
from google import genai

API_KEY = "AIzaSyD7uN5fxjKRUvQM4qQW_bI2xH2xSGn24rM"
client = genai.Client(api_key=API_KEY)

for model in client.models.list():
    if "image" in model.name.lower() or "2.5" in model.name or "2.0" in model.name:
        print(model.name)

import os
import requests
from PIL import Image

HF_API_KEY = os.getenv("HUGGINGFACE_API_KEY")  # Optional for real API use

def generate_description(image_path):
    if HF_API_KEY:
        with open(image_path, "rb") as f:
            image_bytes = f.read()

        response = requests.post(
            "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-base",
            headers={"Authorization": f"Bearer {HF_API_KEY}"},
            data=image_bytes,
        )

        print(f"Response status: {response.status_code}")
        print("Response text:", response.text)  # Add this line to see the problem

        try:
            result = response.json()
            return result[0]["generated_text"]
        except Exception as e:
            print("Failed to parse Hugging Face response:", e)
            return "A wonderful scene captured beautifully."
    else:
        return "A beautiful moment captured with style."

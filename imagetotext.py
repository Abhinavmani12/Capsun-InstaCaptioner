import os
import requests
from PIL import Image

HF_API_KEY = os.getenv("HUGGINGFACE_API_KEY")  # Optional for real API use

def generate_description(image_path):
    if HF_API_KEY:
        # Use Hugging Face Inference API for BLIP model
        with open(image_path, "rb") as f:
            image_bytes = f.read()

        response = requests.post(
            "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-base",
            headers={"Authorization": f"Bearer {HF_API_KEY}"},
            data=image_bytes,
        )

        result = response.json()
        try:
            return result[0]["generated_text"]
        except Exception:
            return "A wonderful scene captured beautifully."
    else:
        # No HF key? Use simple fallback description
        return "A beautiful moment captured with style."

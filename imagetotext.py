import os
import requests
from PIL import Image

HF_API_KEY = os.getenv("HUGGINGFACE_API_KEY")  # Optional if public access works

HF_API_URL = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-base"

def generate_description(image_path):
    try:
        with open(image_path, "rb") as f:
            image_bytes = f.read()

        headers = {"Authorization": f"Bearer {HF_API_KEY}"} if HF_API_KEY else {}
        response = requests.post(HF_API_URL, headers=headers, data=image_bytes)

        print(f"[HuggingFace] Status Code: {response.status_code}")
        print(f"[HuggingFace] Raw Response: {response.text[:200]}")  # Log first 200 chars

        # Parse response safely
        result = response.json()

        if isinstance(result, list) and "generated_text" in result[0]:
            return result[0]["generated_text"]
        elif "error" in result:
            print("❌ HuggingFace Error:", result["error"])
            return "A beautifully captured image, rich in emotion."
        else:
            return "An eye-catching visual scene."

    except Exception as e:
        print("❌ HuggingFace Captioning Failed:", e)
        return "A picture worth a thousand words."

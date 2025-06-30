import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_caption_with_hashtags(description, style):
    prompt = f"""Generate an Instagram caption in a {style} style for the following image description:
'{description}'

Also generate 5 relevant hashtags.
Format the response as:
Caption: <your caption here>
Hashtags: #hashtag1 #hashtag2 ...
"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    full_text = response.choices[0].message.content.strip()

    # Simple parsing
    try:
        caption = full_text.split("Caption:")[1].split("Hashtags:")[0].strip()
        hashtags = full_text.split("Hashtags:")[1].strip()
    except Exception:
        caption = full_text
        hashtags = "#photo #insta"

    return caption, hashtags

import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_caption_with_hashtags(description, style="classic"):
    prompt = {
        "witty": f"Write a witty Instagram caption for this: '{description}', and also suggest 5 relevant hashtags.",
        "emotional": f"Write a heartfelt Instagram caption about: '{description}', and suggest 5 matching hashtags.",
        "poetic": f"Write a poetic Instagram caption about: '{description}', and add 5 beautiful hashtags.",
        "classic": f"Write a simple Instagram caption for: '{description}', and add 5 common relevant hashtags."
    }.get(style, f"Write a cool caption for: '{description}', and add 5 relevant hashtags.")

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )

    content = response['choices'][0]['message']['content']
    
    if "\n" in content:
        parts = content.strip().split("\n")
        caption = parts[0].strip()
        hashtags = "\n".join(parts[1:]).strip()
    else:
        caption = content.strip()
        hashtags = ""

    return caption, hashtags

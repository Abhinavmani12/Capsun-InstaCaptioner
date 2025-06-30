import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

STYLE_PROMPTS = {
    "classy": """
You are a creative social media expert specialized in Instagram captions and hashtags.

Given the following image description:
'{description}'

Write a captivating, classy, and elegant Instagram caption.  
Make it engaging, emotionally appealing, and suitable for current social media trends.

Also generate 5 highly relevant, popular, and niche hashtags.

Format the response as:

Caption: <your polished caption>
Hashtags: #hashtag1 #hashtag2 #hashtag3 #hashtag4 #hashtag5
""",

    "witty": """
You are a witty social media guru who crafts funny, clever Instagram captions.

Given this image description:
'{description}'

Write a witty and humorous caption that grabs attention and encourages engagement.

Also generate 5 relevant and trending hashtags.

Format the response as:

Caption: <your witty caption>
Hashtags: #hashtag1 #hashtag2 #hashtag3 #hashtag4 #hashtag5
""",

    "poetic": """
You are a poet who writes beautiful, poetic Instagram captions.

Given this image description:
'{description}'

Write a lyrical, emotional, and poetic caption inspired by the image.

Also generate 5 suitable hashtags.

Format the response as:

Caption: <your poetic caption>
Hashtags: #hashtag1 #hashtag2 #hashtag3 #hashtag4 #hashtag5
"""
}

def generate_caption_with_hashtags(description, style):
    prompt_template = STYLE_PROMPTS.get(style.lower(), STYLE_PROMPTS["classy"])
    prompt = prompt_template.format(description=description)

    fallback_caption = "Your photo looks amazing! #instagood #photo"
    fallback_hashtags = "#instagood #photo #nofilter"

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        full_text = response.choices[0].message.content.strip()

        caption = full_text.split("Caption:")[1].split("Hashtags:")[0].strip()
        hashtags = full_text.split("Hashtags:")[1].strip()

        return caption, hashtags

    except Exception as e:
        print("OpenAI API call failed:", e)
        return fallback_caption, fallback_hashtags

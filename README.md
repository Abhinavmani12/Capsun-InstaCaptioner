# 📸 InstaCaptioner

**InstaCaptioner** is an AI-powered web app that generates professional Instagram captions and relevant hashtags based on the content of your uploaded images.

---

## 🚀 Features

- 🖼️ Image-to-text analysis using BLIP (Hugging Face)
- ✍️ GPT-3.5-powered caption generation in multiple styles: Classy, Witty, Poetic
- 🔖 Relevant hashtag generation tailored to the caption
- 📲 Share captions instantly via WhatsApp
- 📥 Download your image with overlaid caption and hashtags
- 📅 Schedule Instagram posts via Zapier integration
- 🌙 Toggle between light and dark mode for comfortable usage
- 📱 Fully mobile responsive design
- 🧠 Caption history dashboard to track your previous creations

---

## 💻 Local Setup Instructions

```bash
# Clone the repository
git clone https://github.com/yourusername/instacaptioner.git
cd instacaptioner

# Create and activate a virtual environment
python -m venv venv

# For Linux/macOS:
source venv/bin/activate

# For Windows (PowerShell):
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Set your environment variables (replace with your actual keys)
export OPENAI_API_KEY="your_openai_api_key_here"
export ZAPIER_WEBHOOK_URL="your_zapier_webhook_url_here"   # Optional for scheduling

# Run the app
python app.py

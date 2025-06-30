# 📸 InstaCaptioner

InstaCaptioner is an AI-powered web app that generates Instagram captions and hashtags based on the content of your uploaded image.

---

## 🚀 Features

- 🖼️ Image-to-text analysis (BLIP)
- ✍️ GPT-3.5-powered captions in multiple styles
- 🔖 Hashtag generation
- 📲 WhatsApp sharing
- 📥 Download image with caption
- 📅 Schedule post to Instagram (via Zapier)
- 🌙 Dark mode toggle
- 📱 Mobile responsive
- 🧠 Caption history dashboard

---

## 💻 Local Setup

```bash
git clone https://github.com/yourusername/instacaptioner.git
cd instacaptioner
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export OPENAI_API_KEY=your_openai_key_here
python app.py

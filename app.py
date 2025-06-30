import os
from flask import Flask, request, render_template, redirect, url_for, send_file, flash
from werkzeug.utils import secure_filename
from captioner import generate_caption_with_hashtags
from imagetotext import generate_description
from models import db, CaptionHistory
from datetime import datetime
import requests
import io
from PIL import Image, ImageDraw, ImageFont
from dotenv import load_dotenv

# Load .env variables early
load_dotenv()

UPLOAD_FOLDER = 'static'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

ZAPIER_WEBHOOK_URL = os.getenv("ZAPIER_WEBHOOK_URL", "")
FLASK_SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "supersecretkey")

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///captions.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = FLASK_SECRET_KEY

db.init_app(app)

with app.app_context():
    db.create_all()


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def index():
    caption = None
    hashtags = None
    image_url = None
    style = 'classy'  # default style

    if request.method == 'POST':
        style = request.form.get('style', 'classy')
        file = request.files.get('image')

        if file and allowed_file(file.filename):
            filename = secure_filename("uploaded.jpg")  # Overwrite same file to keep simple
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            try:
                file.save(filepath)
            except Exception as e:
                flash(f"Failed to save the uploaded file: {e}")
                return render_template('index.html', caption=caption, hashtags=hashtags, image_url=image_url, style=style)

            image_url = url_for('static', filename=filename)

            try:
                description = generate_description(filepath)
                caption, hashtags = generate_caption_with_hashtags(description, style)
            except Exception as e:
                caption = "Oops! Couldn’t generate a caption."
                hashtags = "#error #tryagain"
                flash(f"Error during caption generation: {e}")

            # Save entry to DB
            try:
                new_entry = CaptionHistory(
                    image_filename=filename,
                    caption=caption,
                    hashtags=hashtags,
                    style=style,
                    timestamp=datetime.utcnow()
                )
                db.session.add(new_entry)
                db.session.commit()
            except Exception as e:
                flash(f"Database error: {e}")

        else:
            flash("Invalid file type. Please upload a PNG or JPG image.")

    return render_template(
        'index.html',
        caption=caption,
        hashtags=hashtags,
        image_url=image_url,
        style=style
    )


@app.route('/download', methods=['POST'])
def download():
    caption = request.form.get('caption', '')
    hashtags = request.form.get('hashtags', '')
    filename = request.form.get('filename', 'uploaded.jpg')
    img_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    if not os.path.exists(img_path):
        flash("Image file not found for download.")
        return redirect(url_for('index'))

    try:
        img = Image.open(img_path).convert("RGB")
        draw = ImageDraw.Draw(img)
        font = ImageFont.load_default()

        W, H = img.size
        text = caption + "\n\n" + hashtags
        lines = text.split('\n')
        y = 10

        for line in lines:
            w, h = draw.textsize(line, font=font)
            draw.text(((W - w) / 2, y), line, fill="white", font=font)
            y += h + 10

        output = io.BytesIO()
        img.save(output, format='JPEG')
        output.seek(0)
        return send_file(output, download_name="InstaPost.jpg", as_attachment=True)
    except Exception as e:
        flash(f"Error processing image: {e}")
        return redirect(url_for('index'))


@app.route('/schedule', methods=['POST'])
def schedule():
    if not ZAPIER_WEBHOOK_URL:
        return "Zapier scheduling not configured.", 400

    caption = request.form.get('caption', '')
    hashtags = request.form.get('hashtags', '')
    filename = request.form.get('filename', 'uploaded.jpg')
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    if not os.path.exists(image_path):
        return "Image file not found for scheduling.", 400

    try:
        with open(image_path, 'rb') as img_file:
            files = {'file': img_file}
            data = {'caption': caption + "\n\n" + hashtags}
            response = requests.post(ZAPIER_WEBHOOK_URL, data=data, files=files)

        if response.status_code == 200:
            return "✅ Post scheduled successfully via Zapier!"
        else:
            return f"❌ Failed to schedule post. Status code: {response.status_code}", 500
    except Exception as e:
        return f"❌ Error scheduling post: {e}", 500


@app.route('/history')
def history():
    try:
        all_posts = CaptionHistory.query.order_by(CaptionHistory.timestamp.desc()).all()
    except Exception as e:
        flash(f"Failed to load history: {e}")
        all_posts = []
    return render_template('history.html', history=all_posts)


if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)

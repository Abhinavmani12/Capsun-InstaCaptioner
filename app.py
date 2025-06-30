import os
from flask import Flask, request, render_template, redirect, url_for, send_file
from werkzeug.utils import secure_filename
from captioner import generate_caption_with_hashtags
from imagetotext import generate_description
from models import db, CaptionHistory
from datetime import datetime
import requests
import io
from PIL import Image, ImageDraw, ImageFont
from dotenv import load_dotenv

load_dotenv()

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

ZAPIER_WEBHOOK_URL = "https://hooks.zapier.com/hooks/catch/your-zap-url"  # Replace with your actual Zapier webhook URL

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///captions.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

db.init_app(app)

with app.app_context():
    db.create_all()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        style = request.form.get('style', 'classy').lower()
        file = request.files.get('image')

        if not file or file.filename == '':
            return render_template('index.html', error="Please upload an image file.", caption=None)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            description = generate_description(filepath)
            caption, hashtags = generate_caption_with_hashtags(description, style)

            new_entry = CaptionHistory(
                image_filename=filename,
                caption=caption,
                hashtags=hashtags,
                style=style,
                timestamp=datetime.utcnow()
            )
            db.session.add(new_entry)
            db.session.commit()

            image_url = url_for('static', filename=f'uploads/{filename}')

            return render_template('index.html', caption=caption, hashtags=hashtags, style=style, image_url=image_url)
        else:
            return render_template('index.html', error="Invalid file type.", caption=None)

    return render_template('index.html', caption=None, hashtags=None, style=None, image_url=None)

@app.route('/download', methods=['POST'])
def download():
    caption = request.form['caption']
    hashtags = request.form['hashtags']
    filename = request.form['filename']

    img_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    img = Image.open(img_path).convert("RGB")
    draw = ImageDraw.Draw(img)

    try:
        font_path = os.path.join('arial.ttf')  # Make sure arial.ttf is available or specify another font file
        font = ImageFont.truetype(font_path, 20)
    except:
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

@app.route('/schedule', methods=['POST'])
def schedule():
    caption = request.form['caption']
    hashtags = request.form['hashtags']
    filename = request.form['filename']

    image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    with open(image_path, 'rb') as img_file:
        files = {'file': img_file}
        data = {'caption': caption + "\n\n" + hashtags}
        response = requests.post(ZAPIER_WEBHOOK_URL, data=data, files=files)

    if response.status_code == 200:
        return "Post scheduled successfully!"
    return "Failed to schedule post."

@app.route('/history')
def history():
    all_posts = CaptionHistory.query.order_by(CaptionHistory.timestamp.desc()).all()
    return render_template('history.html', history=all_posts)

if __name__ == '__main__':
    app.run(debug=True)

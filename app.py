from flask import Flask, render_template, request, send_file, jsonify
import numpy as np
import cv2
from PIL import Image
import io
from werkzeug.utils import secure_filename

app = Flask(__name__)

def convert_to_pencil_art_balanced(img):
    img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
    inverted = 255 - gray
    blurred = cv2.GaussianBlur(inverted, (21, 21), 0)
    inverted_blur = 255 - blurred
    pencil_sketch = cv2.divide(gray, inverted_blur, scale=256)
    return pencil_sketch

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'image' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    file = request.files['image']
    img = Image.open(file.stream).convert('RGB')
    final_sketch = convert_to_pencil_art_balanced(img)
    pil_sketch = Image.fromarray(final_sketch)
    buf = io.BytesIO()
    pil_sketch.save(buf, format='PNG')
    buf.seek(0)
    return send_file(buf, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)

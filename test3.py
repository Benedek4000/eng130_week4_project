import os
import time
from flask import Flask, request, send_from_directory, jsonify, render_template

image_dir = 'data/images'
os.makedirs(image_dir, exist_ok=True)

app = Flask(__name__)

@app.route('/webcamserver')
def root():
    return render_template('index.html')

@app.route('/webcamserver/download/<image>')
def download(image):
    return send_from_directory(image_dir, image)

@app.route('/webcamserver/upload', methods=['POST'])
def upload(camera_id):
    millis = int(time.time() * 1000)
    fn = f'{image_dir}/{millis}.jpg'
    data = request.get_data()
    with open(fn, 'wb') as f:
        f.write(data)
    return jsonify({'filename': fn})

app.run(host='0.0.0.0', port=5000)
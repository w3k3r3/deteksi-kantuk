from flask import Flask, render_template, request, jsonify, send_file, url_for, redirect
from PIL import Image
import os, io, sys
import numpy as np
import cv2
import base64

from werkzeug.utils import secure_filename, send_from_directory
from yolo_detection import run_model
from language_conversion import convert_lang
import subprocess

app = Flask(__name__)
# Route untuk memproses gambar, menjalankan model deteksi objek, dan konversi bahasa
@app.route('/project_pcd', methods=['POST'])
def mask_image():
    # Membaca file gambar dari request
    file = request.files['image'].read() 
    npimg = np.frombuffer(file,np.uint8)
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)[:, :, ::-1]
    # Menjalankan model deteksi objek
    img,text = run_model(img)
    print("{} This is from app.py".format(text))
    if(text.lower() == "he is"):
        text = ""
    # Menyusun teks dalam bahasa Inggris dan Indonesia
    if(len(text) == 0):
        text = "Reload the page and try with another better image"
    
    englishtext = text
    indotext = convert_lang(text)
    # Mengonversi gambar ke format base64 untuk dikirim sebagai respons JSON
    bufferedBytes = io.BytesIO()
    img_base64 = Image.fromarray(img)
    img_base64.save(bufferedBytes, format="JPEG")
    img_base64 = base64.b64encode(bufferedBytes.getvalue())
    
    return jsonify({'status':str(img_base64),'englishmessage':englishtext, 'indomessage':indotext})

# Route untuk uji coba
@app.route('/test', methods=['GET', 'POST'])
def test():
	print("log: got at test", file=sys.stderr)
	return jsonify({'status': 'succces'}) 

# Route untuk halaman utama
@app.route('/')
def home():
    return render_template('index.html')

# Fungsi untuk menambahkan header CORS setiap kali respons dikirim
@app.after_request
def after_request(response):
    print("log: setting cors", file=sys.stderr)
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers','Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

# Route untuk menjalankan skrip deteksi kamera
@app.route("/opencam", methods=['GET'])
def opencam():
    print("here")
    subprocess.run(['python3', 'detect.py'])
    return "done"

if __name__ == '__main__':
    app.run(host="192.168.238.1", port=8080, debug=False, threaded=False)   #ganti dengan alamat ipmu
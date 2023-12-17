import torch
from matplotlib import pyplot as plt
import numpy as np
import cv2

# Path ke model YOLOv5 yang sudah dilatih
model_name='./yolov5/runs/train/exp/weights/best.pt'
# Memuat model YOLOv5
model = torch.hub.load('./yolov5', 'custom', path=model_name, source='local')
# Menggunakan kamera video (0 menunjukkan kamera default)
cap = cv2.VideoCapture(0)

# Loop untuk membaca setiap frame dari kamera
while cap.isOpened():
    # Membaca frame dari kamera
    ret, frame = cap.read()
    
    # Mendapatkan hasil deteksi objek dari model YOLOv5
    results = model(frame)
    
    # Menampilkan frame dengan hasil deteksi
    cv2.imshow('YOLO', np.squeeze(results.render()))
    
    # Menunggu tombol 'q' untuk keluar dari loop
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break
# Melepaskan kamera dan menutup jendela tampilan
cap.release()
cv2.destroyAllWindows()
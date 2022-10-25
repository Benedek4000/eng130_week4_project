import numpy as np 
import cv2

cap = cv2.VideoCapture(0)

def gen_frames():
    while True:
        r, frame = cap.read()
        if not r:
            break
        else:
            ret, buffer = cv2.imencode(".jpg", frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    

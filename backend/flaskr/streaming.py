import numpy as np 
import cv2
from datetime import datetime as d
import pyaudio
import wave



def gen_frames():
    cap = cv2.VideoCapture(0)
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    now = d.now().strftime("%d%m%y-%H%M%S")
    name = now+".mp4"
    out = cv2.VideoWriter(name, fourcc, 20.0, (640,480))
    

    press = True

    while press:
        r, frame = cap.read()
        if not r:
            break
        elif cv2.waitKey(1) == ord("q"):
            press = False
        else:
            
            ret, buffer = cv2.imencode(".jpg", frame)
            out.write(frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            
    out.release()
    print("this was done after!!!!!!!!!!!!!!!!!!!!!!!!!!")

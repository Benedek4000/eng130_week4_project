import numpy as np 
import cv2
from datetime import datetime as d
import pyaudio
import wave

cap = cv2.VideoCapture(0)
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
now = d.now().strftime("%d%m%y-%H%M%S")
name = now+".mp4"
out = cv2.VideoWriter(name, fourcc, 20.0, (640,480))

chunk = 1024  # Record in chunks of 1024 samples
sample_format = pyaudio.paInt16  # 16 bits per sample
channels = 2
fs = 44100  # Record at 44100 samples per second
seconds = 3
filename = "output.wav"
p = pyaudio.PyAudio()

stream = p.open(format=sample_format,
                channels=channels,
                rate=fs,
                frames_per_buffer=chunk,
                input=True)

frames = []


while True:
    r, frame = cap.read()
    cv2.imshow("my face", frame)
    out.write(frame)
    data = stream.read(chunk)
    frames.append(data)
    if cv2.waitKey(1) == ord("q"):
        break
    
cap.release()
cv2.destroyAllWindows()
out.release()

stream.stop_stream()
stream.close()
# Terminate the PortAudio interface
p.terminate()

# Save the recorded data as a WAV file
wf = wave.open(filename, 'wb')
wf.setnchannels(channels)
wf.setsampwidth(p.get_sample_size(sample_format))
wf.setframerate(fs)
wf.writeframes(b''.join(frames))
wf.close()
print("done")



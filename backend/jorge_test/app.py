import cv2
import datetime, time
import os, sys
import numpy as np
from threading import Thread
from flask import Flask, render_template, Response, request
import pyaudio
import wave

global rec, press, num

rec = "testing again"

num = 0
press = True
app = Flask(__name__)

def change():
    global press
    while press:
        chunk = 1024  # Record in chunks of 1024 samples
        sample_format = pyaudio.paInt16  # 16 bits per sample
        channels = 2
        fs = 44100  # Record at 44100 samples per second
        seconds = 3
        filename = "output.wav"

        p = pyaudio.PyAudio()  # Create an interface to PortAudio

        stream = p.open(format=sample_format,
                        channels=channels,
                        rate=fs,
                        frames_per_buffer=chunk,
                        input=True)

        frames = []  # Initialize array to store frames

        # Store data in chunks for 3 seconds



        while press:
            data = stream.read(chunk)
            frames.append(data)
                
        
        #     data = stream.read(chunk)t
        #     frames.append(data)

        # Stop and close the stream 
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
        


    
        


@app.route("/", methods=["POST", "GET"])
def tasks():
    global press
    if request.method == "POST":
        press = not press

    th = Thread(target = change)
    th.start()
    return render_template("index.html", do=rec)


if __name__ == '__main__':
    app.run()


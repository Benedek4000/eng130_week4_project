import cv2
import datetime, time
import os, sys
import numpy as np
from threading import Thread
from flask import Flask, render_template, Response, request
import pyaudio
import wave
from flask_pymongo import PyMongo






app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:22/video_storage"
mongo = PyMongo(app)


    
        


@app.route("/", methods=["POST", "GET"])
def tasks():
    
    if request.method == "POST":
        m = "./out/hover.mp4"
       
        return "done"

    
    return render_template("v.html")


if __name__ == '__main__':
    app.run(debug=True)


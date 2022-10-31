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
# app.config["MONGO_URI"] = "mongodb://127.0.0.1:272/teams_app"
mongo = PyMongo(app, uri="mongodb://127.0.0.1:252/teams_app")


    
        


@app.route("/", methods=["POST", "GET"])
def tasks():
    
    if request.method == "POST":
        mongo = PyMongo(app, uri="mongodb://127.0.0.1:223/teams_app")
        #m = "./out/hover.mp4"
        mongo.save_file( 'file', request.files['file'])
        # mongo.db.video_storage.insert({'username': request.form.get('username'), 'profile_image_name': request.files['file'].filename })
        m=mongo.db.video_storage.find({"test": "testt"})
        print(m)
        return "done"

    
    return render_template("v.html")


if __name__ == '__main__':
    app.run(debug=True)
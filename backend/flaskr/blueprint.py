from flask import Blueprint, render_template, Response, request
from .streaming2 import gen_frames

views = Blueprint("views", __name__)

@views.route("/")
def home():
    return "This is home!"

@views.route("/index", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        press = True
    return render_template("index.html")
    
@views.route("/video")
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@views.route("/test", methods=["GET", "POST"])
def test():
    global press
    return render_template("test.html")

@views.route("/video-player")
def video():
    return render_template("subindex.html")
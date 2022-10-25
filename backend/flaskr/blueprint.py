from flask import Blueprint, render_template, Response, request
from .streaming import gen_frames

views = Blueprint("views", __name__)

@views.route("/")
def home():
    return "This is home!"

@views.route("/index", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        pres = True
    return render_template("index.html")
    
@views.route("/video")
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@views.route("/test")
def test():
    return render_template("test.html")
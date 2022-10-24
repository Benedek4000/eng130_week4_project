from flask import Blueprint, render_template, Response
from .streaming import gen_frames

views = Blueprint("views", __name__)

@views.route("/")
def home():
    return "This is home!"

@views.route("/index")
def index():
    return render_template("index.html")
    
@views.route("/video")
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
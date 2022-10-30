from flask import Flask, render_template
from flask_pymongo import PyMongo

app = Flask(__name__)
# app.config["MONGO_URI"] = "mongodb://localhost:22/video_storage"
# mongo = PyMongo(app)


@app.route("/", methods=["POST", "GET"])
def app():
    return render_template("v.html")

if __name__ == '__main__':
    app.run()

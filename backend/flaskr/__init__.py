from flask import Flask, Response, render_template

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "ABNSPVARJVNALVUAJFV"
    
    from .blueprint import views
    app.register_blueprint(views, url_prefix="/")

    from .streaming import gen_frames

    @app.route("/index")
    def index():
        return render_template("index.html")
    
    @app.route("/video")
    def video_feed():
        return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

    return app
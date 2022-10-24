from flask import Flask, Response, render_template

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "ABNSPVARJVNALVUAJFV"
    
    from .blueprint import views
    app.register_blueprint(views, url_prefix="/")

    from .streaming import show

    return app
from flask import Flask

global press

press = True

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "ABNSPVARJVNALVUAJFV"
    
    from .blueprint import views
    app.register_blueprint(views, url_prefix="/")

    

    

    return app
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


@app.route('/')
def index():
    return "Welcome to the home page!"


@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')


@app.route('/nav')
def welcome():
    return render_template('index.html')


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/videorec')
def videorec():
    return "This is the video recording page"


@app.route('/storage')
def storage():
    return "This is the Storage page"


if __name__ == '__main__':
    app.run(debug=True)

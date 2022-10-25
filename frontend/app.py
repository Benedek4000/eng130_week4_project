from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


@app.route('/')
def index():
    return "Welcome to the home page!"

<<<<<<< HEAD

@app.route('/login', methods=['GET', 'POST'])
=======
@app.route('/home')
def home():
    return "This is the HOMEPAGE"


@app.route('/login', methods=['GET','POST'])
>>>>>>> eec23ad8a452afd7a638a4a9f08a56a923819b15
def login():
    return render_template('login.html')


<<<<<<< HEAD
=======
@app.route('/signup', methods=['GET','POST'])
def signup():
    return render_template('signup.html')

>>>>>>> eec23ad8a452afd7a638a4a9f08a56a923819b15
@app.route('/nav')
def welcome():
    return render_template('index.html')

<<<<<<< HEAD

@app.route('/home')
def home():
    return render_template('home.html')

=======
>>>>>>> eec23ad8a452afd7a638a4a9f08a56a923819b15

@app.route('/videorec')
def videorec():
    return "This is the video recording page"


@app.route('/storage')
def storage():
    return "This is the Storage page"


if __name__ == '__main__':
    app.run(debug=True)

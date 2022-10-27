from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return 'welcome to practice page'
    else:
        return render_template('login.html')
    
@app.route('/signup', methods=['GET','POST'])
def signup():
    return render_template('signup.html')

@app.route('/forgotPassword', methods=['GET','POST'])
def forgotpassword():
    return render_template('forgotpassword.html')

@app.route('/reset', methods=['GET','POST'])
def reset():
    return render_template('passwordReset.html')


@app.route('/videoplayer')
def player():
    return render_template('video_player.html')


@app.route('/videorec')
def videorec():
    return render_template('video_rec.html')


@app.route('/storage')
def storage():
    return render_template('storage.html')


if __name__ == '__main__':
    app.run(debug=True, port=80)

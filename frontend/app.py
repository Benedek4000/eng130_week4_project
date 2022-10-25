from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        return 'welcome to practice page'
    else:
        return render_template('login.html')

@app.route('/subhaanpractice')
def welcome():
    return 'welcome to subhaans practice page'

if __name__ == '__main__':
    app.run(debug=True)

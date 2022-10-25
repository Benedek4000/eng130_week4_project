# Messing around with some code. Getting use to how to route to urls and so on 
# rendering templates 

from flask import Flask, render_template, url_for
# url_for allows a pages to be switched when a button is clicked  
app = Flask(__name__)

@app.route('/')

def home():
    return render_template('home.html')

@app.route('/login') # this routes to the login page
def login():
    return render_template ('login.html')


@app.route('/register') 
def register():
    return render_template('register.html')


if __name__ == '__main__':
    app.run(debug=True)
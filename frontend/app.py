from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/subhaanpractice')
def welcome():
    return 'Hello this is subhaans practice page'

if __name__ == '__main__':
    app.run(debug=True)

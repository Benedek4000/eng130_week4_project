from flask import Flask, render_template, request
from flask_mail import Mail
from flask_mail import Message


app = Flask(__name__)


app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'mosman196@gmail.com'
app.config['MAIL_PASSWORD'] = 'csmleswbunbxjqhz'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)


@app.route("/", methods=["POST", "GET"])
def index():
    print(request.form)
    if request.method == "POST":
        email = request.form.get("email")
        msg = Message('Password reset', sender='mosman196@gmail.com', recipients=[email])
        msg.body = "Please click on the below link to reset your password"
        mail.send(msg)
        return render_template("r.html")
    return render_template("s.html")




if __name__ == '__main__':
    app.run(debug=True)


from app import mail
#from app.email import send_email
from flask import request, redirect, url_for, render_template, Blueprint
#from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
#from app.models import User
#import flask_login

@app_routes.route('/password_reset', methods=['GET', 'POST'])
def reset():

    if request.method == 'GET':
        return render_template('reset.html')

    if request.method == 'POST':

        email = request.form.get('email')
        user = User.verify_email(email)

        if user:
            send_email(user)

        return redirect(url_for('app_routes.login'))

@app_routes.route('/password_reset_verified/<token>', methods=['GET', 'POST'])
def reset_verified(token):

    user = User.verify_reset_token(token)
    if not user:
        print('no user found')
        return redirect(url_for('app_routes.login'))

    password = request.form.get('password')
    if password:
        user.set_password(password, commit=True)

        return redirect(url_for('app_routes.login'))

    return render_template('reset_verified.html')
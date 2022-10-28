from flask import redirect, url_for, render_template, flash
from connectToPostgreSQL import DBConnector as postgresql
import pandas as pd
from database_properties import postgresql_properties as db_p
from .forms import PasswordForm


@app.route('/reset/<token>', methods=["GET", "POST"])
def reset_token(token):
    # calls the form to input users password

    form = PasswordForm()

    if form.validate_on_submit():

        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        user_password = hashed_password
        # adds the user to the database

        with postgresql(host=db_p['host'], db_name=db_p['db_name'], user=db_p['user'], password=db_p['password'], port=db_p['port']) as db:
            db.execute_query(f"UPDATE Users SET password = '{hash_pw(password)}' WHERE email = '{email}';")


        flash('Your password has been updated! You are now able to log in')
        # takes user to sign in page to use the new password

        return redirect(url_for('login'))

    return render_template('reset.html')


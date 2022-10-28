from flask import redirect, url_for, render_template
from connectToPostgreSQL import DBConnector as postgresql
import pandas as pd
from database_properties import postgresql_properties as db_p
from .forms import PasswordForm


@app.route('/reset/<token>', methods=["GET", "POST"])
def reset_with_token(token):
    try:
        email = ts.loads(token, salt="recover-key", max_age=86400)
    except:
        abort(404) 

    # calls the form to input users password

    form = PasswordForm()

    # if the email matches the one that made the request then it takes the new password

    if form.validate_on_submit():
        user = User.query.filter_by(email=email).first_or_404()

        user.password = form.password.data

        # adds the user to the database

        with postgresql(host=db_p['host'], db_name=db_p['db_name'], user=db_p['user'], password=db_p['password'], port=db_p['port']) as db:
            db.execute_query(f"UPDATE Users SET password = '{hash_pw(password)}' WHERE email = '{email}';")

        # takes user to sign in page to use the new password

        return redirect(url_for('signin'))

    return render_template('reset_with_token.html', form=form, token=token)
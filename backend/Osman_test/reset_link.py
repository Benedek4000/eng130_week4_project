from flask import redirect, url_for, render_template
from connectToPostgreSQL import DBConnector as postgresql
import pandas as pd
from database_properties import postgresql_properties

# request a password reset link

@app.route('/reset', methods=["GET", "POST"])
def reset():
    form = EmailForm()
    if form.validate_on_submit()
        user = User.query.filter_by(email=form.email.data).first_or_404()

        subject = "Password reset requested"

        
        #token = ts.dumps(self.email, salt='recover-key')

        recover_url = url_for(
            'reset_with_token',
            token=token,
            _external=True)

        html = render_template(
            'email/recover.html',
            recover_url=recover_url)

        # send email function
        # return user to main page

        return redirect(url_for('index'))
    return render_template('reset.html', form=form)
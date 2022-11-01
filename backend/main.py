from flask import Flask, request, session, redirect, url_for, render_template, flash
from connectToPostgreSQL import DBConnector as postgresql
import pandas as pd
from database_properties import postgresql_properties_local as psql_prop
#from curses import flash
import hashlib
import re
# from forms import EmailForm, PasswordForm

app = Flask(__name__)
app.secret_key = 'whatever' 

@app.route('/')
def home():
    # Check if user is loggedin
    if 'loggedin' in session:
        # maybe if session.loggedin instaed
    
        # User is loggedin show them the home page
        return render_template('home.html', email=session['email'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@app.route('/login/', methods=['GET', 'POST'])
def login():
    
    #cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    # Check if "email" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        #print(password)
 
        # Check if account exists using MySQL
        #cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        
        with postgresql(host=psql_prop['host'], db_name=psql_prop['db_name'], user=psql_prop['user'], password=psql_prop['password'], port=psql_prop['port']) as db:
            df = db.execute_query('SELECT email, password FROM users WHERE email = %s', (email))

        # Fetch one record and return result
        account = len(df.index)
 
        if account == 1:
            #password_rs = account['password']
            #print(password_rs)
            
            # If account exists in users table in out database
            if hash_pw(password) == df['password']:
                
                # Create session data, we can access this data in other routes
                session['loggedin'] = True
                session['email'] = account['email']
                
                # Redirect to home page
                return redirect(url_for('home'))
            else:
                # Account doesnt exist or username/password incorrect
                flash('Incorrect Email/password')
        else:
            # Account doesnt exist or username/password incorrect
            flash('Incorrect Email/password')
 
    return render_template('login.html')



#------- Register

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    # It is an object that is used to make the connection for executing SQL queries
    #cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
 
    # Check if "email" and "password" POST requests exist 
    
    if request.method == 'POST' and 'password' in request.form and 'email' in request.form:
        
        # Create variables for easy access later on 
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        phone_number = request.form['phone_number']
        password = request.form['password']
        email = request.form['email']
    
        #_hashed_password = hash_pw(password)
 
        #Check if account exists using MySQL
        #cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        with postgresql(host=psql_prop['host'], db_name=psql_prop['db_name'], user=psql_prop['user'], password=psql_prop['password'], port=psql_prop['port']) as db:
            df = db.execute_query('SELECT email FROM users WHERE email = %s', (email))

        account = len(df.index)
        print(account)
        
        # If the account already exist show error and validation checks
        if account > 0:
            flash('Account already exists!')
            
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash('Invalid email address!')
            
        #elif not re.match(,(phone_number)):
            #flash('Invalid phone Number')
        
            
        elif (password is None) or (phone_number is None) or (firstname is None) or (lastname is None):
            flash('Please fill out the form!')
            
        else:
            # Account doesnt exists and the form data is valid, now insert new account into users table
            #cursor.execute("INSERT INTO users (firstname, lastname, phone_number, password, email) VALUES (%s,%s,%s,%s,%s)", (firstname, lastname,phone_number, _hashed_password, email))
            with postgresql(host=psql_prop['host'], db_name=psql_prop['db_name'], user=psql_prop['user'], password=psql_prop['password'], port=psql_prop['port']) as db:
                df = db.execute_query("INSERT INTO users (firstname, lastname, phone_number, password, email) VALUES (%s,%s,%s,%s,%s)", (firstname, lastname,phone_number, hash_pw(password), email))
            flash('You have successfully registered!')
            
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        flash('Please fill out the form!')
        
    # Show registration form with message (if any)
    return render_template('signup.html')


def hash_pw(password, salt="5gz"):
    return hashlib.md5((password+salt).encode().hexdigest())


@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('email', None)
   # Redirect to login page
   return redirect(url_for('login'))


@app.route('/reset', methods=["GET", "POST"])
def reset():
    form = EmailForm()
    if form.validate_on_submit():
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

        #db.session.add(user)
        with postgresql(host=psql_prop['host'], db_name=psql_prop['db_name'], user=psql_prop['user'], password=psql_prop['password'], port=psql_prop['port']) as db:
            df = db.execute_query(f"INSERT INTO Users(email, password, first_name, last_name, phone_number) VALUES ('{user.email}', '{hash_pw(user.password)}', '{user.first_name}', '{user.last_name}', '{user.phone_number}';")

        # takes user to sign in page to use the new password

        return redirect(url_for('signin'))

    return render_template('reset_with_token.html', form=form, token=token)


if __name__ == "__main__":
    app.run(debug=True)
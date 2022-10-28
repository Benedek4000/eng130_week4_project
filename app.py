import hashlib
from flask import Flask, render_template, request, flash,  session, redirect, url_for
from backend.connectToPostgreSQL import DBConnector as postgresql
from backend.database_properties import postgresql_properties_global as psql_prop


import pandas as pd
app = Flask(__name__)
"""
BACKEND STUFF IN FRONTEND FOLDER
Migrate main.py to app.py
"""


@app.route('/')
def home():
    # Check if user is loggedin
    if 'loggedin' in session:

        # User is loggedin show them the home page
        return render_template('home.html', email=session['email'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and 'email' in request.form.get and 'password' in request.form.get:
        email = request.form['email']
        password = request.form['password']

        with postgresql(host=psql_prop['host'], db_name=psql_prop['db_name'], user=psql_prop['user'], password=psql_prop['password'], port=psql_prop['port']) as db:
            df = db.execute_query(
                'SELECT email, password FROM users WHERE email = %s', (email))

        # Fetch one record and return result
        account = len(df.index)

        if account == 1:
            # password_rs = account['password']
            # print(password_rs)

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


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    print(request.form)
    # print(request.form.get)
    print(request.form.get("email"))
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        # create session variables to get into the if statement instead of checking for pass and email
        # Create variables for easy access later on

        print(request.form.get('firstName'))
        print("Setting variables")
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        phone_number = request.form.get('phone_number')
        password = request.form.get('password')
        email = request.form.get('email')

        # Check if account exists using MySQL
        # cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        print("Querying database")
        with postgresql(host=psql_prop['host'], db_name=psql_prop['db_name'], user=psql_prop['user'], password=psql_prop['password'], port=psql_prop['port']) as db:
            df = db.execute_query(
                f"SELECT email FROM users WHERE email = '{email}';")

        account = len(df.index)
        print(account)

        # If the account already exist show error and validation checks
        if account > 0:
            print("Account exists")
            flash('Account already exists!')

        # elif not re.match(,(phone_number)):
            # flash('Invalid phone Number')
        else:
            # Account doesnt exists and the form data is valid, now insert new account into users table
            # cursor.execute("INSERT INTO users (firstname, lastname, phone_number, password, email) VALUES (%s,%s,%s,%s,%s)", (firstname, lastname,phone_number, _hashed_password, email))
            print("Inserting into database")
            with postgresql(host=psql_prop['host'], db_name=psql_prop['db_name'], user=psql_prop['user'], password=psql_prop['password'], port=psql_prop['port']) as db:
                df = db.execute_query(f"INSERT INTO users (firstname, lastname, phone_number, password, email) VALUES ('{firstname}', '{lastname}', '{phone_number}', '{password}', '{email}');")                  
            # flash('You have successfully registered!')
        return render_template("login.html")

    elif request.method == 'POST':
        # Form is empty... (no POST data)
        print("Form not complete")
        # flash('Please fill out the form!')
    print("we good")

    # if request.method == "POST":
    #     return render_template("home.html")

    return render_template('signup.html')


@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
    session.pop('loggedin', None)
    session.pop('email', None)
    # Redirect to login page
    return redirect(url_for('login'))


@app.route('/forgotPassword', methods=['GET', 'POST'])
def forgotpassword():
    # Check if user is loggedin
    # if 'loggedin' in session:
    return render_template('forgotpassword.html')


@app.route('/reset', methods=['GET', 'POST'])
def reset():
    # Check if user is loggedin
    # if 'loggedin' in session:
    return render_template('passwordReset.html')


@app.route('/videoplayer')
def player():
    # Check if user is loggedin
    if 'loggedin' in session:
        return render_template('video_player.html')


@app.route('/videorec')
def videorec():
    # Check if user is loggedin
    if 'loggedin' in session:
        return render_template('video_rec.html')


@app.route('/storage')
def storage():
    # Check if user is loggedin
    if 'loggedin' in session:
        return render_template('storage.html')


def hash_pw(password, salt="5gz"):
    return hashlib.md5((password+salt).encode().hexdigest())


if __name__ == '__main__':
    app.run(debug=True, port=80)
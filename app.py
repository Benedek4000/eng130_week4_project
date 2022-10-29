import hashlib
from urllib import response
# from readline import insert_text
from flask import Flask, render_template, request, flash,  session, redirect, url_for, make_response
from backend.connectToPostgreSQL import DBConnector as postgresql
from backend.database_properties import postgresql_properties_local as psql_prop


import pandas as pd
app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
"""
BACKEND STUFF IN FRONTEND FOLDER
Migrate main.py to app.py
"""


@app.route('/')
def home():
    
    # Check if user is loggedin
    #if request.cookies.get('email') != None:
    
    if 'loggedin' in session and session['loggedin']:
        # User is loggedin show them the home page
        return render_template('home.html', last_name=session['last_name'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))



@app.route('/login', methods=['GET', 'POST'])
def login():
    
    if request.cookies.get('email') != None:
        print(request.cookies.get('email'))
        return redirect(url_for('home'))

    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form.get('email')
        password = request.form.get('password')
        with postgresql(host=psql_prop['host'], db_name=psql_prop['db_name'], user=psql_prop['user'], password=psql_prop['password'], port=psql_prop['port']) as db:
            df = db.execute_query(
                f"SELECT email, password, last_name, user_id FROM users WHERE email = '{email}'")

        # Fetch one record and return result
        
        if len(df.index) == 1:
            # password_rs = account['password']
            # print(password_rs)
            # If account exists in users table in out database
            if hash_pw(password) == df.iloc[0,1]:

                # Create session data, we can access this data in other routes
                session['loggedin'] = True
                session['email'] = df.iloc[0,0]
                session['last_name'] = df.iloc[0,2]
                session['id'] = str(df.iloc[0,3])
                

                # respo = make_response(render_template('login.html'))
                # respo.set_cookie('email', email)
                
                # Redirect to home page
                flash("Logged in success", category="true")
                
                return redirect(url_for("home"))
            else:
                # Account doesnt exist or username/password incorrect
                flash('Incorrect Email/password', category='error')
        else:
            # Account doesnt exist or username/password incorrect
            flash('Incorrect Email/password', category='error')

    return render_template("login.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    
    print(request.cookies.get("valid"))

    if 'loggedin' in session and session['loggedin']==True:
        # User is loggedin show them the home page
        return redirect(url_for('home'))

    if request.method == 'POST' and request.cookies.get("valid") == "true":
        # create session variables to get into the if statement instead of checking for pass and email
        # Create variables for easy access later on
        
        print("\n ========================= \n")
        print(request.form.get('firstName'))
        
        print("Setting variables")
        
        firstname = request.form.get('firstName')
        lastname = request.form.get('lastName')
        phone_number = request.form.get('phoneNum')
        password = request.form.get('password')
        email = request.form.get('email')

        # Check if account exists using MySQL
        # cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        print("\n ========================= \n")
        print("Querying database")
        with postgresql(host=psql_prop['host'], db_name=psql_prop['db_name'], user=psql_prop['user'], password=psql_prop['password'], port=psql_prop['port']) as db:
            df = db.execute_query(
                f"SELECT email FROM users WHERE email = '{email}';")

        #account = len(df.index)
        #print(account)

        # If the account already exist show error and validation checks
        if len(df.index) > 0:
            
            flash('Account already exists!', category="error")

        # elif not re.match(,(phone_number)):
            # flash('Invalid phone Number')
        else:
            # Account doesnt exists and the form data is valid, now insert new account into users table
            # cursor.execute("INSERT INTO users (firstname, lastname, phone_number, password, email) VALUES (%s,%s,%s,%s,%s)", (firstname, lastname,phone_number, _hashed_password, email))
            
            
            print("Inserting into database")
            with postgresql(host=psql_prop['host'], db_name=psql_prop['db_name'], user=psql_prop['user'], password=psql_prop['password'], port=psql_prop['port']) as db:
                df = db.execute_query(f"INSERT INTO users (first_name, last_name, phone_number, password, email) VALUES ('{firstname}', '{lastname}', '{phone_number}', '{hash_pw(password)}', '{email}');")                  
            flash('You have successfully registered!', category="true")
            return redirect(url_for('login'))

    elif request.method == 'POST' and request.cookies.get("valid") == "false":
        # Form is empty... (no POST data)
        
        flash('Please fill out the form!', category="error")

    # if request.method == "POST":
    #     return render_template("home.html")

    return render_template('signup.html')


@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
    session.pop('loggedin', None)
    session.pop('email', None)
    session.pop('last_name', None)
    session.pop('id', None)
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

@app.route("/test/<t>")
def test(t):
    m = t
    print(t)
    return f"test {m}"


def hash_pw(password, salt="5gz"):
    return hashlib.md5((password+salt).encode()).hexdigest()


if __name__ == '__main__':
    app.run(debug=True, port=80)

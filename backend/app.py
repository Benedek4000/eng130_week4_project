from flask import Flask, request, session, redirect, url_for, render_template, flash
from connectToPostgreSQL import DBConnector as postgresql
import pandas as pd
from database_properties import postgresql_properties_local as psql_prop
#from curses import flash
import hashlib
import re

app = Flask(__name__)
app.secret_key = 'whatever' 

@app.route('/')

def home():
    # Check if user is loggedin
    if 'loggedin' in session:
    
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

if __name__ == "__main__":
    app.run(debug=True)
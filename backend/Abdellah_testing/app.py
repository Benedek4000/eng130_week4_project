from flask import Flask, request, session, redirect, url_for, render_template, flash
from connectToPostgreSQL import DBConnector as postgresql
import pandas as pd
from database_properties import postgresql_properties
from curses import flash

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
    
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
   
    # Check if "email" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        print(password)
 
        # Check if account exists using MySQL
        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        
        # Fetch one record and return result
        account = cursor.fetchone()
 
        if account:
            password_rs = account['password']
            print(password_rs)
            
            # If account exists in users table in out database
            if check_password_hash(password_rs, password):
                
                # Create session data, we can access this data in other routes
                session['loggedin'] = True
                session['id'] = account['id']
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

@app.route('/register', methods=['GET', 'POST'])
def register():
    # It is an object that is used to make the connection for executing SQL queries
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
 
    # Check if "email" and "password" POST requests exist 
    
    if request.method == 'POST' and 'password' in request.form and 'email' in request.form:
        
        # Create variables for easy access later on 
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        phone_number = request.form['phone_number']
        password = request.form['password']
        email = request.form['email']
    
        _hashed_password = generate_password_hash(password)
 
        #Check if account exists using MySQL
        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        account = cursor.fetchone()
        print(account)
        
        # If the account already exist show error and validation checks
        if account:
            flash('Account already exists!')
            
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash('Invalid email address!')
            
        elif not re.match(,(phone_number)):
            flash('Invalid phone Number')
        
            
        elif not password or not email:
            flash('Please fill out the form!')
            
        else:
            # Account doesnt exists and the form data is valid, now insert new account into users table
            cursor.execute("INSERT INTO users (firstname, lastname, phone_number, password, email) VALUES (%s,%s,%s,%s,%s)", (firstname, lastname,phone_number, _hashed_password, email))
            conn.commit()
            flash('You have successfully registered!')
            
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        flash('Please fill out the form!')
        
    # Show registration form with message (if any)
    return render_template('register.html')

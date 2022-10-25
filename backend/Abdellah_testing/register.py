@app.route('/register', methods=['GET', 'POST'])
def register():
    # cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
 
    
    if request.method == 'POST' and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
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
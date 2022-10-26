# Messing around with some code. Getting use to how to route to urls and so on 
# rendering templates  

from flask import Flask, render_template, url_for
# url_for allows a pages to be switched when a button is clicked  
app = Flask(__name__)

@app.route('/')

def home():
    return render_template('home.html')

@app.route('/login') # this routes to the login page
def login():
    return render_template ('login.html')


@app.route('/register') 
def register():
    return render_template('register.html')


if __name__ == '__main__':
    app.run(debug=True)
    
# ---------------------------------------------------------------------------------------------------

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
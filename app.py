import os, sys
import hashlib
import urllib.request
from urllib import response
from flask import Flask, render_template, request, flash,  session, redirect, url_for, make_response, Response, jsonify
sys.path.insert(0, './backend')
from connectToPostgreSQL import DBConnector as postgresql
from database_properties import postgresql_properties_local as psql_prop
import S3 as s3
from flask_mail import Mail
from flask_mail import Message
import datetime, time
from werkzeug.utils import secure_filename
import pandas as pd
from threading import Thread as th


app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
"""
BACKEND STUFF IN FRONTEND FOLDER
Migrate main.py to app.py
"""
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'mosman196@gmail.com'
app.config['MAIL_PASSWORD'] = 'csmleswbunbxjqhz'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['UPLOAD_FOLDER'] = './static/uploads/'
#app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

mail = Mail(app)

#make shots directory to save pics, temp files and videos
try:
    os.mkdir("./static/uploads")
except OSError as error:
    pass

global postgres_ip, postgres_port, bucket_name
bucket_name=os.environ.get("BUCKET")

foo = os.environ.get("POSTGRES")
if foo:
    end = foo.find(':', 10)
    postgres_ip = foo[11:end]
    postgres_port = foo[end+1:]
else:
    postgres_ip = psql_prop['host']
    postgres_port = psql_prop['port']

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
    global postgres_ip, postgres_port

    if 'loggedin' in session and session['loggedin']:
        flash("Already logged in!", category="error")
        return redirect(url_for("home"))
    if request.cookies.get('email') != None:
        print(request.cookies.get('email'))
        return redirect(url_for('home'))

    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form.get('email')
        password = request.form.get('password')
        with postgresql(host=postgres_ip, db_name=psql_prop['db_name'], user=psql_prop['user'], password=psql_prop['password'], port=postgres_port) as db:
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
                print(session['id'])
                

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
    global postgres_ip, postgres_port
    
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
        with postgresql(host=postgres_ip, db_name=psql_prop['db_name'], user=psql_prop['user'], password=psql_prop['password'], port=postgres_port) as db:
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
            with postgresql(host=postgres_ip, db_name=psql_prop['db_name'], user=psql_prop['user'], password=psql_prop['password'], port=postgres_port) as db:
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
    global postgres_ip, postgres_port
    # Check if user is loggedin
    if 'loggedin' in session and session['loggedin']:
        return redirect(url_for("home"))
    elif request.method == "POST" and "email" in request.form:
        email = request.form.get("email")
        
        with postgresql(host=postgres_ip, db_name=psql_prop['db_name'], user=psql_prop['user'], password=psql_prop['password'], port=postgres_port) as db:
            df = db.execute_query(
                f"SELECT email FROM users WHERE email = '{email}';")
        if len(df.index) == 0:
            flash('Account does not exists!', category="error")
        elif len(df.index) > 0:
            x=np.random.randint(99, size=(29))
            y=''.join(map(str, x))
            msg = Message('Password reset', sender='eng130Test@gmail.com', recipients=[email])
            if os.environ.get('MY_IP'):
                msg.body = f"Please click on the link to reset your password: http://{os.environ.get('MY_IP')}/reset/{y}"
            else:
                msg.body = f"Automated Server IP identification was refused, please use this link as a base format for the url to reset your password: http://host_ip/reset/{y}"
            mail.send(msg)
            
            with postgresql(host=postgres_ip, db_name=psql_prop['db_name'], user=psql_prop['user'], password=psql_prop['password'], port=postgres_port) as db:
                db.execute_query(f"UPDATE Users SET password_reset = '{y}' WHERE email = '{email}';")
            flash("Email has been sent, please check your email.", category="true")
            
            return redirect(url_for("login"))
    return render_template('forgotpassword.html')

global email

@app.route('/reset/<r>', methods=['GET', 'POST'])
def reset(r):
    global email, postgres_ip, postgres_port
    # Check if user is loggedin
    if 'loggedin' in session and session['loggedin']:
        return redirect(url_for("home"))
    if request.method == "POST" and request.form.get("password") == request.form.get("confirmPassword"):
        new_password = request.form.get("password")
        with postgresql(host=postgres_ip, db_name=psql_prop['db_name'], user=psql_prop['user'], password=psql_prop['password'], port=postgres_port) as db:
                db.execute_query(f"UPDATE Users SET password = '{hash_pw(new_password)}' WHERE email = '{email}';")
        flash("Password has been reset", category="true")
        return redirect(url_for("home"))
    elif request.form.get("password") != request.form.get("confirmPassword"):
        flash("Password don't match", category="error")
        return render_template("passwordReset.html")


    if len(r)<10:
        flash("Invalid link", category="error")
        return redirect(url_for("home"))
    else:
        reset = r
        with postgresql(host=postgres_ip, db_name=psql_prop['db_name'], user=psql_prop['user'], password=psql_prop['password'], port=postgres_port) as db:
            df = db.execute_query(
                f"SELECT email FROM users WHERE password_reset = '{reset}';")
        if len(df.index) == 0:
            flash("Invalid link", category="error")
            return redirect(url_for("home"))
        else:
            email = df.iloc[0,0]
            print(email)
            with postgresql(host=postgres_ip, db_name=psql_prop['db_name'], user=psql_prop['user'], password=psql_prop['password'], port=postgres_port) as db:
                db.execute_query(f"UPDATE Users SET password_reset = 'FALSE' WHERE email = '{email}';")
            return render_template('passwordReset.html')


    
    
    return render_template('passwordReset.html')


@app.route('/videoplayer')
def player():
    # Check if user is loggedin
    if 'loggedin' in session and session['loggedin']:
        return render_template('video_player.html')
    else:
        flash("You need to be logged in to use this website", category="error")
        return redirect(url_for("login"))
global data
# data = ip(output = 'json')
data = "coming soon"
@app.route('/videorec', methods=["POST", "GET"])
def videorec():
    if 'loggedin' in session and session['loggedin']:
        
        return render_template('video2.html')
        
    else:
        flash("You need to be logged in to use this website", category="error")
        return redirect(url_for("login"))


@app.route('/storage', methods=["POST", "GET"])
def storage():
    global postgres_ip, postgres_port, bucket_name
    
    # Check if user is loggedin
    if 'loggedin' in session and session['loggedin']:
        if request.method == "POST":
            object = request.form.get('Delete')
            s3.delete_file(bucket_name, object)
            with postgresql(host=postgres_ip, db_name=psql_prop['db_name'], user=psql_prop['user'], password=psql_prop['password'], port=postgres_port) as db:
                df = db.execute_query(
                    f"DELETE FROM Videos WHERE video_title = '{object}';")

        with postgresql(host=postgres_ip, db_name=psql_prop['db_name'], user=psql_prop['user'], password=psql_prop['password'], port=postgres_port) as db:
            df = db.execute_query(
                f"SELECT video_link FROM Videos WHERE user_id = {session['id']};")
        print(len(df.index))
        if len(df.index) == 0:
            no_links = "You yet to make a video"
            return render_template('video_player.html', no_links = no_links)
        li = list(df.to_dict()[0].values())
        name = []
        for n in li:
            name.append([ n, os.path.split(n)[1]])
        return render_template('video_player.html', name = name)
    else:
        flash("You need to be logged in to use this website", category="error")
        return redirect(url_for("login"))

@app.route('/test', methods=["POST", "GET"])
def test():
    return render_template('video2.html')
@app.route('/test2', methods=["POST", "GET"])
def test2():
    return render_template('video3.html')

@app.route('/upload', methods=['POST'])
def upload():
    global postgres_ip, postgres_port, bucket_name
    file = request.files['file']
    if file:
        now = datetime.datetime.now().strftime("%d%m%yI%H%M%S")
        filename = session['id']+"I"+now+".mp4"
        id = session['id']
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #file.save(os.path.join('./', filename))
        # uploading to s4 bucket
        th(target= s3_upload, args=[filename, id]).start()
        # process the file object here! 
        return jsonify(success=True)
    return jsonify(success=False)
def s3_upload(filename, id):
    s3.upload(f'./static/uploads/{filename}', bucket_name,object_name=filename)
    os.remove(f"./static/uploads/{filename}")
    id = int(id)
    with postgresql(host=postgres_ip, db_name=psql_prop['db_name'], user=psql_prop['user'], password=psql_prop['password'], port=postgres_port) as db:
        print("in with")
        try:    
            df = db.execute_query(f"INSERT INTO Videos (video_title, video_link, user_id) VALUES ('{filename}', 'https://eng130-videos.s3.eu-west-1.amazonaws.com/{filename}', {id});")
        except:
            raise Exception()

    


def hash_pw(password, salt="5gz"):
    return hashlib.md5((password+salt).encode()).hexdigest()


if __name__ == '__main__':
    app.run(debug=True, port=80, host='0.0.0.0')

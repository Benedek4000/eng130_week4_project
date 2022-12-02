import os, sys
import os, sys
import hashlib
from urllib import response
# from readline import insert_text
from flask import Flask, render_template, request, flash,  session, redirect, url_for, make_response, Response
# sys.path.insert(0, './backend')
from backend.connectToPostgreSQL import DBConnector as postgresql
from backend.connectToMongoDB import DBConnector as mongodb
from backend.database_properties import postgresql_properties_global as psql_prop, mongodb_properties_global as db_m
from flask_mail import Mail
from flask_mail import Message
import cv2
import datetime, time

import numpy as np
import pandas as pd
from threading import Thread
# import pyaudio
import wave
import moviepy.editor as m
from ipapi import location as ip
import gridfs
from pymongo import MongoClient

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

mail = Mail(app)

global capture,rec_frame, grey, switch, neg, rec, out, detection, mute, color
color = "#007fff"
capture=0
grey=0
neg=0
switch=1
rec=0
mute = False

#make shots directory to save pics, temp files and videos
try:
    os.mkdir("./shots")
except OSError as error:
    pass

try:
    os.mkdir("./in")
except OSError as error:
    pass

try:
    os.mkdir("./static/out")
except OSError as error:
    pass

camera = cv2.VideoCapture(0)

def record(out):
    global rec_frame, detection
    
    while(rec):
        time.sleep(0.045)
        out.write(rec_frame)
    if mute:
        v = m.VideoFileClip("./in/temp.avi")
        e = v.fx(m.vfx.speedx, 1)
        now = datetime.datetime.now().strftime("%d%m%y-%H%M%S")
        name = "./out/"+now+".mp4"
        e.write_videofile(name, fps = 20)
        


def change(p, stream, frames):
    global rec, mute
    while rec and not mute:
        # chunk = 1024  # Record in chunks of 1024 samples
        # sample_format = pyaudio.paInt16  # 16 bits per sample
        # channels = 2
        # fs = 44100  # Record at 44100 samples per second
        # seconds = 3
        

        # p = pyaudio.PyAudio()  # Create an interface to PortAudio

        # stream = p.open(format=pyaudio.paInt16,
        #                 channels=2,
        #                 rate=44100,
        #                 frames_per_buffer=2,
        #                 input=True)

        # Initialize array to store frames

        # Store data in chunks for 3 seconds



        while rec:
            data = stream.read(1024)
            frames.append(data)
                
        
        #     data = stream.read(chunk)t
        #     frames.append(data)
        filename = "./in/temp.wav"
        # Stop and close the stream 
        stream.stop_stream()
        stream.close()
        # Terminate the PortAudio interface
        p.terminate()

        # Save the recorded data as a WAV file
        wf = wave.open(filename, 'wb')
        wf.setnchannels(2)
        wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
        wf.setframerate(44100)
        wf.writeframes(b''.join(frames))
        wf.close()

        ed = Thread(target = audio_speed)
        ed.start()
        return

def joining():
    v = m.VideoFileClip("./in/temp.avi")
    a = m.AudioFileClip("./in/temp.mp3")
    f = v.set_audio(a)
    now = datetime.datetime.now().strftime("%d%m%y-%H%M%S")
    name = "./static/out/"+now+".mp4"
    f.write_videofile(name, fps = 20)
    # with mongodb(host=db_m['host'], port=db_m['port'], db_name=db_m['db_name'], collection=db_m['collection']) as db:
    #     db.insert_video(email=session['email'], video_file_name=name, video_id=now)

    return

def audio_speed():
    v = m.VideoFileClip("./in/temp.avi")
    a = m.AudioFileClip("./in/temp.wav")
    f = a.duration/v.duration
    e = a.fx(m.vfx.speedx, f)
    e.write_audiofile("./in/temp.mp3")

    jo = Thread(target = joining)
    jo.start()

    return


def gen_frames():  # generate frame by frame from camera
    global out, capture,rec_frame, grey, detection
    # camera = cv2.VideoCapture(0)
    while True:
        success, frame = camera.read() 
        if success:
            detection = True
            if(grey):
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            if(neg):
                frame=cv2.bitwise_not(frame)    
            if(capture):
                capture=0
                now = datetime.datetime.now()
                p = os.path.sep.join(['shots', "shot_{}.png".format(str(now).replace(":",''))])
                cv2.imwrite(p, frame)
            
            if(rec):
                rec_frame=frame
                frame= cv2.putText(cv2.flip(frame,1),"Recording...", (0,25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255),4)
                frame=cv2.flip(frame,1)
            
                
            try:
                ret, buffer = cv2.imencode('.jpg', cv2.flip(frame,1))
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            except Exception as e:
                pass
                
        else:
            detection = False
            flash("Can not detect Camera", category="error")
            pass


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

    if 'loggedin' in session and session['loggedin']:
        flash("Already logged in!", category="error")
        return redirect(url_for("home"))
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

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


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
    if 'loggedin' in session and session['loggedin']:
        return redirect(url_for("home"))
    elif request.method == "POST" and "email" in request.form:
        email = request.form.get("email")
        
        with postgresql(host=psql_prop['host'], db_name=psql_prop['db_name'], user=psql_prop['user'], password=psql_prop['password'], port=psql_prop['port']) as db:
            df = db.execute_query(
                f"SELECT email FROM users WHERE email = '{email}';")
        if len(df.index) == 0:
            
            
            flash('Account does not exists!', category="error")
        elif len(df.index) > 0:
            x=np.random.randint(99, size=(29))
            y=''.join(map(str, x))
            msg = Message('Password reset', sender='mosman196@gmail.com', recipients=[email])
            msg.body = f"Please click on the link to reset your password: http://127.0.0.1:80/reset/{y}"
            mail.send(msg)
            
            with postgresql(host=psql_prop['host'], db_name=psql_prop['db_name'], user=psql_prop['user'], password=psql_prop['password'], port=psql_prop['port']) as db:
                db.execute_query(f"UPDATE Users SET password_reset = '{y}' WHERE email = '{email}';")
            flash("Email has been sent, please check your email.", category="true")
            
            return redirect(url_for("login"))




    return render_template('forgotpassword.html')

global email

@app.route('/reset/<r>', methods=['GET', 'POST'])
def reset(r):
    global email
    # Check if user is loggedin
    if 'loggedin' in session and session['loggedin']:
        return redirect(url_for("home"))
    if request.method == "POST" and request.form.get("password") == request.form.get("confirmPassword"):
        new_password = request.form.get("password")
        with postgresql(host=psql_prop['host'], db_name=psql_prop['db_name'], user=psql_prop['user'], password=psql_prop['password'], port=psql_prop['port']) as db:
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
        with postgresql(host=psql_prop['host'], db_name=psql_prop['db_name'], user=psql_prop['user'], password=psql_prop['password'], port=psql_prop['port']) as db:
            df = db.execute_query(
                f"SELECT email FROM users WHERE password_reset = '{reset}';")
        if len(df.index) == 0:
            flash("Invalid link", category="error")
            return redirect(url_for("home"))
        else:
            email = df.iloc[0,0]
            print(email)
            with postgresql(host=psql_prop['host'], db_name=psql_prop['db_name'], user=psql_prop['user'], password=psql_prop['password'], port=psql_prop['port']) as db:
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
data = ip(output = 'json')

@app.route('/videorec', methods=["POST", "GET"])
def videorec():
    global color, data
    # data = ip(output = 'json')
    if 'loggedin' in session and session['loggedin']:
        global switch,camera
        if request.method == 'POST':
            global rec
            if request.form.get('click') == 'Capture':
                global capture
                capture=1
            elif  request.form.get('grey') == 'Grey':
                global grey
                grey=not grey
            elif  request.form.get('neg') == 'Negative':
                global neg
                neg=not neg
            elif  request.form.get('mute') == 'mute' and not rec:
                global mute, color
                
                if mute:
                    mute = not mute
                    color = "#007fff"
                else:
                    mute = True
                    color = "red"
            elif request.form.get('mute') == 'mute' and rec:
                flash("Can not mute/unmute when video is recording", category="error")
                
                
               
            elif  request.form.get('stop') == 'Stop/Start':
                
                if(switch==1):
                    switch=0
                    camera.release()
                    cv2.destroyAllWindows()
                    
                else:
                    camera = cv2.VideoCapture(0)
                    switch=1
            elif  request.form.get('rec') == 'Start/Stop Recording':
                global out, frames, p, stream
                rec= not rec
                if(rec):
                    
                    
                    fourcc = cv2.VideoWriter_fourcc(*'XVID')
                    # out = cv2.VideoWriter('vid_{}.avi'.format(str(now).replace(":",'')), fourcc, 20.0, (640, 480))
                    out = cv2.VideoWriter('./in/temp.avi', fourcc, 20, (640, 480))
                    #Start new thread for recording the video

                    #audio
                    p = pyaudio.PyAudio()
                    stream = p.open(format=pyaudio.paInt16, channels=2, rate=44100, frames_per_buffer=2, input=True)
                    frames = []
                    thread = Thread(target = record, args=[out,])
                    thread.start()
                    audio = Thread(target = change, args=[p, stream, frames,])
                    audio.start()
                elif(rec==False):
                    
                    out.release()
                    
                            
                    
        elif request.method=='GET':
            return render_template('video_rec.html', color = color, data = data, name = session['last_name'])
        
        return render_template('video_rec.html', color = color, data = data, name = session['last_name'])
        
    else:
        flash("You need to be logged in to use this website", category="error")
        return redirect(url_for("login"))


@app.route('/storage')
def storage():
    
    # Check if user is loggedin
    if 'loggedin' in session and session['loggedin']:
        li = os.listdir('./static/out')
        



        return render_template('video_player.html', videos = li)
    else:
        flash("You need to be logged in to use this website", category="error", name = session['last_name'])
        return redirect(url_for("login"))




def hash_pw(password, salt="5gz"):
    return hashlib.md5((password+salt).encode()).hexdigest()


if __name__ == '__main__':
    app.run(debug=True, port=5000)

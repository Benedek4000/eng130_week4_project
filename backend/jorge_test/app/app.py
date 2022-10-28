from flask import Flask, render_template, Response, request, url_for
import cv2
import datetime, time
import os, sys
import numpy as np
from threading import Thread
import pyaudio
import wave
import moviepy.editor as m


global capture,rec_frame, grey, switch, neg, face, rec, out, frames, p, stream
capture=0
grey=0
neg=0
face=0
switch=1
rec=0



#make shots directory to save pics
try:
    os.mkdir(url_for("./shots"))
except OSError as error:
    pass

try:
    os.mkdir(url_for("./in"))
except OSError as error:
    pass

try:
    os.mkdir(url_for("./out"))
except OSError as error:
    pass

#Load pretrained face detection model    


#instatiate flask app  
app = Flask(__name__, template_folder='./templates')


camera = cv2.VideoCapture(0)

def record(out):
    global rec_frame
    
    while(rec):
        time.sleep(0.045)
        out.write(rec_frame)

def change(p, stream, frames):
    global rec
    while rec:
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
    name = "./out/"+now+".mp4"
    f.write_videofile(name, fps = 20)
    # with mongodb(host=db_m['host'], port=db_m['port'], db_name=db_m['db_name'], collection=db_m['collection']) as db:
    #   ids = db.insert_documents([{'user_id': INSERT USERID HERE, 'filename': INSERT FILENAME HERE, 'file': INSERT FILE HERE}])
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
    global out, capture,rec_frame
    while True:
        success, frame = camera.read() 
        if success:
            
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
            pass


@app.route('/')
def index():
    return render_template('video.html')
    
    
@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/requests',methods=['POST','GET'])
def tasks():
    global switch,camera
    if request.method == 'POST':
        if request.form.get('click') == 'Capture':
            global capture
            capture=1
        elif  request.form.get('grey') == 'Grey':
            global grey
            grey=not grey
        elif  request.form.get('neg') == 'Negative':
            global neg
            neg=not neg
        elif  request.form.get('face') == 'Face Only':
            global face
            face=not face 
            if(face):
                time.sleep(4)   
        elif  request.form.get('stop') == 'Stop/Start':
            
            if(switch==1):
                switch=0
                camera.release()
                cv2.destroyAllWindows()
                
            else:
                camera = cv2.VideoCapture(0)
                switch=1
        elif  request.form.get('rec') == 'Start/Stop Recording':
            global rec, out, frames, p, stream
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
        return render_template('index.html')
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
    
camera.release()
cv2.destroyAllWindows()     
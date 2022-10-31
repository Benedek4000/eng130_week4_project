# Camera module
This is the introduction on how the camera works and help with the understanding of the codes.<br/>
For this part of the website, we will be using the opencv module as it has some easy features that can be implemented or also include some features that can be used in the future. For example Face detection, blurring or removing background.
## Libraries needed
just be running
```bash
pip install -r requirements.txt
```
should be able to install all requirements needed for this application. If no .txt is found, here is the list needed for the camera module only:
- opencv-python # to read and detect camera hardware
- pyaudio # to read and detect audio hardware
- moviepy # to edit and combine both audio and video
- flask # website framework

With all of this, one should be able to run the app.py shown inside this folder.
## Functions
To make certain functions remember a variable and be used or edited in another function, we will be using the `global` so that this is possible. All of the global variable that will be needed for this module is shown below. and give them a starting value that will be read as soon as the server starts running. `0 = False and 1 = True`
```python
global capture,rec_frame, grey, switch, neg, rec, out, frames, p, stream
capture=0
grey=0
neg=0
face=0
switch=1
rec=0
```
We will also create folders to put in these videos, we can create folder using the os function as shown below. The `try` is to ensure to only make a folder if one does not yet exist, if it does exist, this will come as an error and this excepts it and continues with the other codes without breaking the server.
```python
try:
    os.mkdir("./shots")
except OSError as error:
    pass

try:
    os.mkdir("./in")
except OSError as error:
    pass

try:
    os.mkdir("./out")
except OSError as error:
    pass
```
## The camera
As stated from the introduction, we will be using opencv, to be able to detect the camera, we use the function "VideoCapture" inside the cv2 function of opencv.
```python
camera = cv2.VideoCapture(0)
```
The `int` inside the function can be used to altered from 1 camera and another if available. We can also pass a location of a video e.g. "./videos/testing_camera.mp4" so we can render that video and create frames out of that. For this purpose, we will use to detect the camera.

```python
def gen_frames():  # generate frame by frame from camera
    global out, capture,rec_frame
    while True:
        success, frame = camera.read() 
        if success:
            
            if(grey): #change frame/video to black and white
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            if(neg):
                frame=cv2.bitwise_not(frame)    
            if(capture):# takes a picture upon request
                capture=0
                now = datetime.datetime.now()
                p = os.path.sep.join(['shots', "shot_{}.png".format(str(now).replace(":",''))])
                cv2.imwrite(p, frame)
            
            if(rec): # Start the recording function
                rec_frame=frame # two images, one will be manipulated so one can show the recording and the other will be the one used to write the video.
                frame= cv2.putText(cv2.flip(frame,1),"Recording...", (0,25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255),4)
                frame=cv2.flip(frame,1)
            
                
            try:# tries to encode the video format into a readable format for the webpage
                ret, buffer = cv2.imencode('.jpg', cv2.flip(frame,1))
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            except Exception as e:# if no frame is detected, it will pass   without breaking or giving an error
                pass
                
        else:# if no image is being detected py camera, it will pass
            pass
```
Now so that the functions can be changed by the user, we will get options from the client using "POST" method. This will allow the different options available can be altered from a post request that the server gets from the client.
```python
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
            
```
When a post request is sent to the server, it will change the global variable that will alter or take actions upon a request.<br/>
inside the last `elif request.form.get('rec').....` we will add the function to start recording taking frames and recording this into a file so user can safe it and view it in the future.
this can be done by going 
```python 
        elif  request.form.get('rec') == 'Start/Stop Recording': # as shown in the last script
            global rec, out, frames, p, stream # as shown in the last script
            rec= not rec # as shown in the last script
            
            if(rec): # new script
                #if rec is on, record function will start
                fourcc = cv2.VideoWriter_fourcc(*'XVID')
                # fourcc is the video format code and out is the file that will be written
                out = cv2.VideoWriter('./in/temp.avi', fourcc, 20, (640, 480))
                #Start new thread for recording the video

                #audio
                p = pyaudio.PyAudio() # detects audio hardware
                stream = p.open(format=pyaudio.paInt16, channels=2, rate=44100, frames_per_buffer=2, input=True)# function to read the format, speed quality etc.
                frames = [] # an empty list to store audio
                thread = Thread(target = record, args=[out,])
                thread.start() # this will start both audio recording frame and audio recording frame inside these variable and each one will be past to the new function
                audio = Thread(target = change, args=[p, stream, frames,])
                audio.start()
            elif(rec==False): # if rec is off, the file will be released
                
                out.release()
```
Thread is used to start function independently in the background. 
Both of these function are simple, all it does is from the `rec_frame` which is the video frame, will be stored as a video using the `out` function from opencv that we took as a args for this `record` function.
```python
def record(out):
    global rec_frame
    # test_frame=[]
    while(rec):
        time.sleep(0.045)# speed of video. less means video will be shorter/speeded
        out.write(rec_frame)
    return

def change(p, stream, frames):
    global rec
    while rec:
        while rec:
            data = stream.read(1024)# reads audio
            frames.append(data) # add audio inside a list
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

```
The code above, will store both audio and video files into two separated files, to fix this, a background function will be started called audio_speed. The only purpose for this function is to makes sure both the speed of the audio and the speed of the video are the same. and we use the speed of the video as reference. The library used is `moviepy.editor as m`
```python
def audio_speed():
    v = m.VideoFileClip("./in/temp.avi")
    a = m.AudioFileClip("./in/temp.wav")
    f = a.duration/v.duration # finds the ratio of both files respect to video file
    e = a.fx(m.vfx.speedx, f) # takes the f variable to make sure this new file is of the same length as video file
    e.write_audiofile("./in/temp.mp3")

    jo = Thread(target = joining)
    jo.start() # starts the function to integrate both this files as one video file

    return
```
Using the same library, we can integrated the audio as a background sound for the video
```python
def joining():
    v = m.VideoFileClip("./in/temp.avi")
    a = m.AudioFileClip("./in/temp.mp3")
    f = v.set_audio(a) # sets the audio as background
    now = datetime.datetime.now().strftime("%d%m%y-%H%M%S") # sets a time stamp as a name
    name = "./out/"+now+".mp4"
    f.write_videofile(name, fps = 20)
    return
```
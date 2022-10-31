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
## The camera
As stated from the introduction, we will be using opencv, to be able to detect the camera, we use the function "VideoCapture" inside the cv2 function of opencv.
```python
camera = cv2.VideoCapture(0)
```
The int inside the function can be used to altered from 1 camera and another if available. We can also pass a location of a video e.g. "./videos/testing_camera.mp4"

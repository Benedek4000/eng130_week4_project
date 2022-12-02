# Video Recording app

![Alt text](/images/homepage.png)

#### Contributors:

|                         Frontend                         |                             Backend                              |                       Database                       |
| :------------------------------------------------------: | :--------------------------------------------------------------: | :--------------------------------------------------: |
|     [Abishek Aneese](https://github.com/AbisheK0726)     | [Abdelleh Chehat Bais Pedros](https://github.com/AbdellahChehat) |  [Abishek Jha](https://github.com/abhishek-jha-ce)   |
| [Mohamed Abdikarim Yusuf](https://github.com/MoeShaa123) |         [Bendek Kovacs](https://github.com/Benedek4000)          |   [Angel Gelemerov](https://github.com/AGelemerov)   |
|      [Subhaan Hussain](https://github.com/Subzy132)      |           [Jorge Reyes ](https://github.com/Jorge2091)           | [Aenugu Meghana](https://github.com/meghanasrividya) |

## Introduction

Welcome to eng130 Video Recording app project. In this short introduction, we will inform you on how to get the website integrated in your system with simple steps (as long as our public server is running).

## Running on localhost

The list of requirements needed for this website is listed in requirements.txt, all you need to do is clone this repository into your local machine and `cd eng130_week4_project` to get into the folder.

1. After that is done, run the installation by writing in the command line

```bash
pip install -r requirements.txt
```

2. Once all is installed, run the app.py by either doing it through vscode or any other software or writing in the command line:

```bash
python app.py
```

**NOTE: If python doesn't work try python3**

```bash
python3 app.py
```

3. If everything runs as expected you should see this in the terminal

```bash
 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 931-387-081
```

### Running App using Docker

1. Download `Docker` on your machine using the official documentation [Docker](https://www.docker.com)
2. Setup your account and docker desktop and run `docker --version` and you should see

```bash
Docker version 20.10.21, build baeda1f
```

3. Now that you have Docker installed Run the image the app is on

```bash
docker run -d -p 5000:5000 abishek726/test-python-app-111
```

4. If you got to `localhost:5000` in the browser the website should be running

## Toolset

**Draw.io** - A visual diagram creation service that allowed us to draw the mockups and wireframes needed to plan how our application will look. We able draw the different aspects of the app and then annotate it where needed.

![Alt text](/images/wireframes/VideoPlayer.png)

**Python** - The fundamental programming language we used to write our funtionalities. We Imported many API's and Libraries provided by python to carry out different functions.

```python
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
```

**Flask** - A web framework provided by python to allow us to structure our app. It allowed us to easily develop our application using a python file. As long as we had the required dependencies we were able to just run one command and then the app would start.

```bash
python app.py
```

**HTML/CSS** - Python flask allowed us to run our HTML files. These html files were also linked to bootstrap which implemented CSS into our website. What this essentially means is that it makes our website look nice. HTML is the skeleton, CSS is the design(skin) and the javascript carries out the functionality.

```html
<!DOCTYPE html>
<html>
	<head>
		<title>Our Funky HTML Page</title>
		<meta name="description" content="Our first page" />
		<meta name="keywords" content="html tutorial template" />
	</head>
	<body>
		Content goes here.
	</body>
</html>
```

**Javascript** - As mentioned before Javascript carries out some of the functionalities on the HTML templates. We mainly used it on our `login` and `signup` pages as validation. So we used Javascript to validate the user entries before they are actually submitted. Such as: password length, email characters and number digits etc. 

```javascript
function validateSignUpForm() {
	// Get the email and password from the form
	var firstName = document.getElementById('firstName').value;
	var lastName = document.getElementById('lastName').value;
	var email = document.getElementById('email').value;
	var phone = document.getElementById('phoneNum').value;
	var password = document.getElementById('password').value;
	var comPassword = document.getElementById('confirmPassword').value;
	
```

**Docker** - Once we created our application and had it working on the localhost we wanted to containerise the application and the database. and the easiest way to do this was to use Docker which is a platform to deliver software in packages. All we had to do was create Docker files and then upload the image onto dockerhub. 

```dockerfile
FROM python as py

WORKDIR /usr/src/app
COPY requirements.txt ./

RUN apt update && apt upgrade -y
RUN apt-get install libasound-dev portaudio19-dev libportaudio2 libportaudiocpp0 -y

RUN pip install pymongo
RUN pip install pyaudio --user
RUN pip install flask
RUN pip install opencv-python
RUN pip install moviepy
RUN pip install Flask-Mail
RUN pip install pandas
RUN pip install ipapi
RUN pip install "opencv-python-headless<4.3"
RUN pip install psycopg2


COPY . .

EXPOSE 5000

CMD [ "python", "./app.py" ]
```

**Github** - Our version control service. All of the contributors used this to update and test the code we made. we had multiple branches such as the main, test, backend and frontend and database. each tested their code on their branch and then we slowly integrated all the branches into main to create the application. 

**Opencv** - This is a programming library that is aimed at real-time computer vision. Computer vision is a process by which we can understand the images and videos how they are stored and how we can manipulate and retrieve data from them. So we used it to build our camera function. We implemented it with out python flask and we able to build the recording functionality with it using the user's camera module. 

```python
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
```

**Mongodb** - This is the database program we were originally going to use to store the video footage coming from the application usign GridFS but towards the end of the project we quickly realised that it is not compatible with our flask application so we had to scrap that utility and then use Javascript and S3 buckets to store the videos. 


**POSTGRESQL** - This was our relational database system. We used it to hold all the information to do with our users such as the login details, sign-up details. So anything to do with the user. The information was stored here. 

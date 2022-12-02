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

**Javascript** - As mentioned before Javascript carries out some of the functionalities on the HTML templates. We mainly used it on our `login` and `signup` pages as validation. so we

###### Docker

###### Github

###### Opencv

Mongodb


used mongodb
for saving videos using gridfs
wasnt compatible with python flask

SQL


user data
postgress sql 

**S3**
# Video Recording App

![Homepage](/images/homepage.png)

**Contributors:**
|                         Frontend                         |                             Backend                              |                       Database                       |
| :------------------------------------------------------: | :--------------------------------------------------------------: | :--------------------------------------------------: |
|     [Abishek Aneese](https://github.com/AbisheK0726)     | [Abdelleh Chehat Bais Pedros](https://github.com/AbdellahChehat) |  [Abishek Jha](https://github.com/abhishek-jha-ce)   |
| [Mohamed Abdikarim Yusuf](https://github.com/MoeShaa123) |         [Bendek Kovacs](https://github.com/Benedek4000)          |   [Angel Gelemerov](https://github.com/AGelemerov)   |
|      [Subhaan Hussain](https://github.com/Subzy132)      |           [Jorge Reyes ](https://github.com/Jorge2091)           | [Aenugu Meghana](https://github.com/meghanasrividya) |

## Introduction

Welcome to eng130 Video Recording app project. In this short introduction, we will inform you on how to get the website integrated in your system with simple steps (as long as our public server is running).

## Get Started

The next few steps will help you get started with installing the website on your local machine or on a virtual machine and running it.

### Setting environment variables

On your local machine you can add the following environment variables:

```bash
export BUCKET=eng130-videos
export aws_access_key_id=YOUR_KEY
export aws_secret_access_key=YOUR_SECRET_KEY
```

If you are using your aws instance, you can add the following in a file called `.env`:

```bash
BUCKET=eng130-videos
AWS_ACCESS_KEY=YOUR_KEY
AWS_SECRET_KEY=YOUR_SECRET_KEY
```

### Running on localhost

The list of requirements needed for this website is listed in requirements.txt, all you need to do is clone this repository into your local machine. Once you have cloned the repository, you can run following commands

1. Install all the requirements

```bash
pip install -r requirements.txt
```

2. Run the app.py file by running the following command in the terminal or a text editor

```bash
python app.py
```

**NOTE: If python doesn't work try python3.**

```bash
python3 app.py
```

3. A successful run should give you the following output

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

### Running App using Docker on local host or AWS instance

1. For Windows users, install `Docker Desktop` on your machine using the official documentation [Docker Desktop](https://docs.docker.com/docker-for-windows/install/)

2. For AWS users on Linux, install `Docker` on your machine using the official documentation [Docker](https://docs.docker.com/engine/install/ubuntu/)

3. Once install run `docker --version` in terminal to check if docker is installed

```bash
# Expected output
Docker version 20.10.21, build baeda1f 
```

3. With docker running, run the following command in terminal

```bash
cd docker-compose
docker-compose up --remove-orphans
```

4. If you go to `localhost` in the browser the website should be running

### Enable your camera on chrome

Chrome has a feature that blocks access to your camera by default. This should only affect you if you are running the app on your virtual machine with HTTP.

To enable it, go to `chrome://flags/#unsafely-treat-insecure-origin-as-secure` and add `http://<your-VM-ip>`.

Then restart chrome.

## ERD Diagram

Our appliction has database that stores the user information and the videos links that the user records. The database is designed using Postgres.

The Entiy Relationship Diagram (ERD) diagram for the database is shown below.

![ERD](/images/dbdiagram.png)

## Test Cases

| Test scenario | Test Case | Expected Result | Actual Result |
|:-----------: | :----------: | :-------: | :---------: |
|Check Sign Up Functionality| When the user clicks on Register here and enters the submit button without filling in all fields | The user is prompted to enter all fields |[Test 1 Result](/images/tests/test1.png)|
|Check Sign Up Functionality|When the user clicks on Register here and enters the submit button after filling in all fields with the correct information|The user can successfully register|[Test 2 Result](/images/tests/test2.png)|
|Check Sign Up Functionality|When the user clicks on Register here and enters the details that were already registered|The user is prompted the account already exists|[Test 3 Result](/images/tests/test3.png)|
|Check Login Functionality|Login with a valid username and valid password|The user can successfully login|[Test 4 Result](/images/tests/test4.png)|
|Check Login Functionality|Login with an invalid username and invalid password|The user is prompted Incorrect Email/password|[Test 5 Result](/images/tests/test5.png)|
|Check Camera Functionality|When the user clicks on the Start Camera button|The user could be able to start the camera|[Test 6 Result](/images/tests/test6.png)|
|Check Camera Functionality|When the user clicks on the Start Recording button|The user could be able to start the recording and stop recording it should make a recording|[Test 7 Result](/images/tests/test7.png) <br> [Test 8 Result](/images/tests/test8.png)|
|Check Video Storage functionality|When the user clicks on the Storage tab|The user could be able to view the videos that he stored|[Test 9 Result](/images/tests/test9.png)|
|Check the logout functionality|When the user clicks on the logout tab|The user is navigated back to login page|User successfully logged out|

## Toolset

### Draw.io

A visual diagram creation service that allowed us to draw the mockups and wireframes needed to plan how our application will look. We able draw the different aspects of the app and then annotate it where needed.

![Video Player Wireframe](/images/wireframes/VideoPlayer.png)

### Python

The fundamental programming language we used to write our funtionalities. We use a python framework called Flask to structure our application and create the backend.

We Imported many API's and Libraries provided by python to carry out different functions, such as.

```python
import os
from flask import Flask, render_template, request, flash,  session, redirect, url_for, make_response, Response
from flask_mail import Mail
import cv2
import datetime, time
```

### Flask

A web framework provided by python to allow us to structure our app. It allowed us to easily develop our application using a python file. As long as we had the required dependencies we were able to just run one command and then the app would start.

### HTML/CSS

Python flask allowed us to run our HTML files. These html files were also linked to bootstrap which implemented CSS into our website. What this essentially means is that it makes our website look nice. HTML is the skeleton, CSS is the design(skin) and the javascript carries out the functionality.

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

### Javascript

As mentioned before Javascript carries out some of the functionalities on the HTML templates. We mainly used it on our `login` and `signup` pages as validation. So we used Javascript to validate the user entries before they are actually submitted. Such as: password length, email characters and number digits etc. 

```javascript
function validateLoginForm() {
   // Get the email and password from the form
   var email = document.getElementById('email').value;
   var password = document.getElementById('password').value;
   
   // Check if email and password is empty
   if (email == '' || password == '') {
      // Return Error Message if email and password is empty
      alert('Please enter your email and password');
      return false;
   } else {
      return true;
   }
}
```

### Docker

Once we created our application and had it working on the localhost we wanted to containerise the application and the database. and the easiest way to do this was to use Docker which is a platform to deliver software in packages. All we had to do was create Docker files and then upload the image onto dockerhub.

```dockerfile
FROM python:slim
LABEL MAINTERNER=jorge2091/t
WORKDIR /usr/src/app
COPY . .
RUN python -m pip install psycopg2-binary
RUN ["/bin/bash", "-c", "apt update"]
RUN ["/bin/bash", "-c", "apt install libpq-dev -y"]
RUN ["/bin/bash", "-c", "apt install build-essential -y"]
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 80
CMD [ "python", "app.py" ]
```

### Github

Our version control service. All of the contributors used this to update and test the code we made. we had multiple branches such as the main, test, backend and frontend and database. Each group tested their code on their branch and then we slowly integrated all the branches into main to create the application.

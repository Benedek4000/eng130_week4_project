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


FROM python:3.10.8-bullseye

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN apt update
RUN apt install build-essential
RUN pip install --upgrade pip
RUN pip install gcc7
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

COPY --from=py /usr/src/app /usr/src/app

EXPOSE 5000

CMD [ "python", "./app.py" ]
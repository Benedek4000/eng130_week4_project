FROM python:3
LABEL MAINTERNER=jorge2091/test
WORKDIR /usr/src/app
COPY . .
RUN apt update
RUN apt upgrade -y
RUN apt-get install libasound-dev portaudio19-dev libportaudio2 libportaudiocpp0 -y
RUN pip install pyaudio --user
RUN pip install -r requirements.txt
RUN pip install "opencv-python-headless<4.3"
EXPOSE 80
CMD [ "python", "./app.py" ]
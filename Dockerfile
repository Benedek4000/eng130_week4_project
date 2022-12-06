FROM python:slim
LABEL MAINTERNER=jorge2091/test
WORKDIR /usr/src/app
COPY . .
RUN python -m pip install psycopg2-binary
RUN ["/bin/bash", "-c", "apt update"]
RUN ["/bin/bash", "-c", "apt install libpq-dev -y"]
RUN ["/bin/bash", "-c", "apt install build-essential -y"]
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 80
CMD [ "python", "app.py" ]
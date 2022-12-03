FROM python:3
LABEL MAINTERNER=jorge2091/test
WORKDIR /usr/src/app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 80
CMD [ "python", "app.py" ]
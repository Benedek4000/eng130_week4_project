# Using pymongo and gridfs to store and retrieve video files from a MongoDB database
# Steps:
# 1. Connect to MongoDB
# 2. Create a new database
# 3. Create a new collection
# 4. Create a new GridFS object
# 5. Store a video file in GridFS
# 6. Retrieve the video file from GridFS
# 7. Save the video file to disk (optional)

from pymongo import MongoClient
from gridfs import GridFS

def mongo_connect():
    try:
        conn = MongoClient(host='86.191.168.203', port=27017)
        print ("Connected successfully!!!", conn)
        return conn.gridfs_test
    except Exception as e:
        print ("Could not connect to MongoDB", e)
        
db = mongo_connect()

name = 'text.txt'
file_location = './' + name
file_data = open(file_location, 'rb')
data = file_data.read()
fs = GridFS(db)
try:
    fs.put(data, filename=name)
    print ("File saved successfully")
except Exception as e:
    print ("Could not save file to MongoDB", e)


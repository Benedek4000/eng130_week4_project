# by Benedek Kovacs

import pymongo
import sys
import moviepy.editor as mp
import pickle
from bson.binary import Binary
from connectToPostgreSQL import DBConnector as postgresql
from database_properties import postgresql_properties_local as db_p
from tqdm import tqdm


# class used to connect to a mongodb database
class DBConnector:

    #used for print(db) 
    def __str__(self):
        return 60*'-'+'\n'+'\n'.join(f"email: {i['email']}   video_id: {i['video_id']}   frame_no: {i['frame_no']}" for i in self.coll.find({}))+'\n'+60*'-'

    # enable usage of 'with'
    def __enter__(self):
        return self

    # runs upon end of 'with'
    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.close_db()

    # initialise connection to database
    def __init__(self, host, port, db_name, collection):
        try:
            self.client = pymongo.MongoClient(f'mongodb://{host}:{port}')
            self.db = self.client[db_name]
            self.coll = self.db[collection]
            print('Successfully connected to MongoDB Platform')
        except Exception as e:
            print(f'Error connecting to MongoDB Platform: {e}')
            sys.exit(1)

    # close connection to database
    def close_db(self):
        if self.client is not None:
            try:
                self.client.close()
                print('Database connection closed.')
            except Exception as e:
                print(f'Error closing connection to MongoDB Platform: {e}')
        else:
            print('Connection does not exist.')

    # get documents from database. returns zero, one or more documents
    def get_video(self, video_id):
        try:
            frames = []
            for frame in tqdm(self.coll.find({'video_id': video_id}).sort('frame_no', 1).allow_disk_use(True)):
                frames.append(pickle.loads(frame['frame']))
            return mp.ImageSequenceClip(frames, fps=20)
            #return mp.ImageSequenceClip(list(pickle.loads(frame['frame']) for frame in self.coll.find({'video_id': video_id}).sort('frame_no', 1).allow_disk_use(True)), fps=20)
        except Exception as e:
            print(f"Error retrieving data from MongoDB: {e}")
            return None

    # insert one or more documents to database. returns inserted IDs
    def insert_video(self, email, video_file_name, video_id=None):  # pass document(s) as a dictionary or as a list of dictionaries
        try:
            with postgresql(host=db_p['host'], db_name=db_p['db_name'], user=db_p['user'], password=db_p['password'], port=db_p['port']) as dbsql:
                clip = mp.VideoFileClip(video_file_name).subclip(0,3)
                frames = list(value for value in clip.iter_frames())
                del clip
                df = dbsql.execute_query(f"SELECT object_id FROM Videos WHERE email = '{email}'")
                if video_id == None:    
                    if df.empty:
                        video_id = 1
                    else:
                        video_id = max(int(value) for value in df.iloc[:,0].to_list()) + 1
                dbsql.execute_query(f"INSERT INTO Videos(email, object_id) VALUES ('{email}', '{video_id}')")
                docs_to_insert = []
                for index, frame in enumerate(frames):
                    docs_to_insert.append({'email': email, 'video_id': video_id, 'frame_no': index, 'frame': Binary(pickle.dumps(frame, protocol=2), subtype=128 )})
                self.coll.insert_many(docs_to_insert)
            return None
        except Exception as e:
            print(f"Error inserting data into MongoDB: {e}")
            return None
# by Benedek Kovacs

import pymongo
import gridfs
import sys
from bson.objectid import ObjectId
from connectToPostgreSQL import DBConnector as postgresql
from database_properties import postgresql_properties_local as db_p


# class used to connect to a mongodb database
class DBConnector:

    #used for print(db) 
    def __str__(self):
        return 60*'-'+'\n'+'\n'.join(str(i) for i in self.fs.list())+'\n'+60*'-'

    # enable usage of 'with'
    def __enter__(self):
        return self

    # runs upon end of 'with'
    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.close_db()

    # initialise connection to database
    def __init__(self, host, port, db_name):
        try:
            self.client = pymongo.MongoClient(f'mongodb://{host}:{port}')
            self.db = self.client[db_name]
            self.fs = gridfs.GridFS(self.db)
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
    def get_video(self, object_id):
        try:
            return self.fs.get(ObjectId(object_id))
        except Exception as e:
            print(f"Error retrieving data from MongoDB: {e}")
            return None

    # insert one or more documents to database. returns inserted IDs
    def insert_video(self, email, video_file):  # pass document(s) as a dictionary or as a list of dictionaries
        try:
            with postgresql(host=db_p['host'], db_name=db_p['db_name'], user=db_p['user'], password=db_p['password'], port=db_p['port']) as db:
                db.execute_query(f"INSERT INTO Videos(email, object_id) VALUES ('{email}', '{(self.fs.put(data=video_file))}')")
            return None
        except Exception as e:
            print(f"Error inserting data into MongoDB: {e}")
            return None
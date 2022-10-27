# by Benedek Kovacs

import pymongo
import sys
from bson.objectid import ObjectId


# class used to connect to a mongodb database
class DBConnector:
    
    # enable usage of 'with'
    def __enter__(self):
        return self

    # runs upon end of 'with'
    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.close_db()

    # initialise connection to database
    def __init__(self, host, port, db_name, collection):
        try:
            #self.client = pymongo.MongoClient(f'mongodb://{user}:{password}@{host}:{port}')
            self.client = pymongo.MongoClient(host, int(port))
            self.db = self.client[db_name]
            self.coll = self.db[collection]
            print('Successfully connected to MongoDB Platform')
        except pymongo.errors as e:
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
    def get_documents(self, key='_id', value=None):
        try:
            if key == '_id':
                documents = self.coll.find({key: ObjectId(value)})
            else:
                documents = self.coll.find({key: value})
            return documents
        except Exception as e:
            print(f"Error: {e}")
            return e

    # insert one or more documents to database. returns inserted IDs
    def insert_documents(self, documents):  # pass document(s) as a dictionary or as a list of dictionaries
        try:
            return self.coll.insert_many(documents).inserted_ids
        except Exception as e:
            print(f"Error: {e}")
            return e
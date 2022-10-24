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
    def __init__(self, host, port, db_name):
        try:
            #self.client = pymongo.MongoClient(f'mongodb://{host}:{port}')
            self.client = pymongo.MongoClient(host, port)
            self.db = self.client[db_name]
            print('Successfully connected to MongoDB Platform')
        except pymongo.Error as e:
            print(f'Error connecting to MongoDB Platform: {e}')
            sys.exit(1)

    # close connection to database
    def close_db(self):
        if self.client is not None:
            try:
                self.client.close()
                print('Database connection closed.')
            except pymongo.Error as e:
                print(f'Error closing connection to MongoDB Platform: {e}')
        else:
            print('Connection does not exist.')

    # get documents from database. returns zero, one or more documents
    def getDocuments(self, key='_id', value=None):
        try:
            if key == '_id':
                documents = self.db.posts.find({key: ObjectId(value)})
            else:
                documents = self.db.posts.find({key: value})
            return documents
        except pymongo.Error as e:
            print(f"Error: {e}")
            return e

    # insert one or more documents to database. returns inserted IDs
    def insertDocuments(self, *documents):
        try:
            return self.db.posts.insert_many(documents).inserted_ids
        except pymongo.Error as e:
            print(f"Error: {e}")
            return e
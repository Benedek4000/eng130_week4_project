# Backend

## Databases

### Connecting to Databases

#### Connecting to PostgreSQL

Use `connectToPostgreSQL.py` to connect to PostgreSQL database.

example code to execute a query:
```python
from connectToPostgreSQL import DBConnector as postgresql

with postgresql(host='localhost', db_name='users', user='postgres', password='Abcd1234', port=1234) as db:
    df = db.executeQuery('QUERY HERE')
```

#### Connecting to MongoDB

Use `connectToMongoDB.py` to connect to MongoDB database.

example code to get zero, one or more documents:
```python
from connectToMongoDB import DBConnector as mongodb
from bson.objectid import ObjectId

with mongodb(host='localhost', db_name='recordings', port=1234) as db:
    documents = getDocuments(key='_id', value=ObjectId(post_id))
    # or documents = getDocuments(value=ObjectId(post_id)), as default value for key: key='_id'
```

## Front end

### Login page

Features I'll need to include in the log in page 
- email input
- password input 
- forgot password
- sign in button 
- sign up button
  

  
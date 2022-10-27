# Backend

## Databases

### Connecting to Databases

#### Connecting to PostgreSQL

Use `connectToPostgreSQL.py` to connect to PostgreSQL database.

example code to execute a query:
```python
from connectToPostgreSQL import DBConnector as postgresql
import pandas as pd
from database_properties import postgresql_properties

with postgresql(host='127.0.0.1', db_name='users', user='postgres', password='spartaglobal', port='22') as db:
    db.execute_query("INSERT INTO Users(email, password, first_name, last_name, is_admin) VALUES ('bkovacs@spartaglobal.com', 'psswrd', 'Benedek', 'Kovacs', false);")
    df = db.execute_query('SELECT * FROM Users;')
    print(df)
    db.execute_query("INSERT INTO Sessions(user_id, location) VALUES (1, 'United Kingdom');")
    df = db.execute_query('SELECT * FROM Sessions;')
    print(df)
```

to print the whole database, use `print(db)`

#### Connecting to MongoDB

Use `connectToMongoDB.py` to connect to MongoDB database.

example code to get zero, one or more documents:
```python
from connectToMongoDB import DBConnector as mongodb
from bson.objectid import ObjectId

with mongodb(host='localhost', db_name='teams_app', collection='video_storage', port='22') as db:
    documents = get_documents(key='_id', value=target_value)  # to return all documents, value=None
```

example code to insert one or more documents:
```python
from connectToMongoDB import DBConnector as mongodb
from bson.objectid import ObjectId

with mongodb(host='localhost', db_name='teams_app', collection='video_storage', port='22') as db:
    inserted_ids = insert_documents(documents)  # type of documents is list
```

to print the whole collection, use `print(db)`

## Front end

### Login page

Features I'll need to include in the log in page 
- email input
- password input 
- forgot password
- sign in button 
- sign up button
  

  
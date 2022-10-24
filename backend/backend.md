# Backend

## Databases

### Connecting to Databases

#### Connecting to PostgreSQL

Use `connectToPostgreSQL.py` to connect to PostgreSQL database.

example code:
```python
with DBConnector(host="localhost", db_name="suppliers", user="postgres", password="Abcd1234", port=1234) as db:
    df = db.executequery("QUERY HERE")
```

#### Connecting to MongoDB

Use `connectToMongoDB.py` to connect to MongoDB database.

## Front end

### Login page

Features I'll need to include in the log in page 
- email input
- password input 
- forgot password
- sign in button 
- sign up button
  

  
# DB / #

- We will use SQL to query for data
  - Flat file database for recordings
    - No repetitions anyway due to location, time stamps
  - Relational database to store user information
- We will use (most likely) MongoDB for both databases
  - We have used it and linked it before so will be relatively easy to do

## Relational database / ##

We will use PostgreSQL for the relational database as it offers a lot of features like SQL querying, API support, migration to bigger databases and is supported on many operating systems
`https://db-engines.com/en/system/PostgreSQL`

# DB
### What is MongoDB?

- It is a NoSQL database called (Document database)

- It stores data in flexible JSON - like document

- It is higly scalable and flexible database.

### How MongoDB looks when compared to RDBMS

- In RDBMS the data is stored in tables, whereas in MONGODB the data is stored in JSON format. 

###  The Structure of MongoDB database:

- MongoDB physical database contain several logical databases.

- Each database contain several collections. Collection is something like table in relational database.

- Each collection contains several documents. Document is something like record or row in RDBMS.

### Key Characteristics of MongoDB database:

- Installation and setup is very easy

- All information related to a document is stored in a single place.

- MongoDB has a restriction of each document size to be 16 MB. But you can store large files like audio/video files using GridFS.

- Files are "chunked" into multiple objects that are less than 255 KiB each. This has the added advantage of letting us efficiently retrieve a specific range of the given file.


### GridFS:

- GridFS basically takes afile and breaks it up into multiple chiunks which are stored as individual documents in two collectobs:

 - the chunk collection (stores the document parts), and

 - the file collection (stores the consequent additional metadata)


 - Each chunk is limited to 255 KB in size. This means that the last chunk is normally either equal to or less than 255KB 


 - When you read from GridFS , the driver reassembles all the chunks as needed. This means that you can read sections of a file as per your query range.

<<<<<<< HEAD
 - 
=======
Picture for ERD
>>>>>>> 1092e9db8b8229d012ae787733eb37bf2fd453ad

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

## How to setup VM with ssh and sftp

- install SSH
  - `sudo apt update`
  - `sudo apt upgrade`
  - `sudo apt install openssh-server`
  - `sudo service ssh status`
  - if not running start service with
    - `sudo service ssh start`
  - make sure it is running (`sudo service ssh status`)
  - enable firewall for specified port from status command
    - `sudo ufw allow ssh`
    - `sudo ufw enable`
    - `sudo ufw status`
      - you should see port 22 there
    - get your local IP address
      - `ifconfig` (install if you dont have it)
  - install PuTTY and connect to db
  - `sudo adduser sftp_user` any name works, this is just placeholder
  - for ease of use you can set password to be the same as username
  - no further details needed apart from password
  - `sudo mkdir -p /var/sftp/myfolder/data`
  - `sudo chown root:root: /var/sftp/myfolder`
  - `sudo chmod 755 /var/sftp/myfolder`
  - `sudo chown sftp_user:sftp_user /var/sftp/myfolder/data`
  - `sudo nano /etc/ssh/sshd_config`
    - write the following lines at the very bottom of the file
    - `Port <your_port_number>`
    - `Match User sftp_user`
    - `ForceCommand internal-sftp`
    - `PasswordAuthentication yes`
    - `ChrootDirectory /var/sftp/myfolder`
    - `PermitTunnel no`
    - `AllowAgentForwarding no`
    - `AllowTcpForwarding no`
    - `X11Forwarding no`
  - we will need to now restart the ssh service to read this additional data
    - `sudo /etc/init.d/ssh restart`


## NoSQL Database

- We are using `MongoDB` as the `NoSQL` database to store the video files.

### What is MongoDB?

- It is a NoSQL database called (Document database)

- It stores data in flexible "JSON-like" document.

- It is higly scalable and flexible database, perfect for our scenario.

### Why MongoDB?

- Installation and setup is very easy

- All information related to a document is stored in a single place.

### Structure & Comparision with `RDBMS`

- MongoDB physical database contains several logical databases.

- Each database contain several `collections`. Collection is similar to table in relational database.

- Each `collection` contains several `documents`. Document is similar to record or row in RDBMS.

- In RDBMS the data is stored in tables, whereas in MONGODB the data is stored in JSON format.

### Problems

The maximum BSON document size is 16 megabytes.

The maximum document size helps ensure that a single document cannot use excessive amount of RAM or, during transmission, excessive amount of bandwidth.

### Solution - `GridFS API`

To store documents larger than the maximum size of 16 megabytes, MongoDB provides the GridFS API

- GridFS basically takes a file and breaks it up into multiple chunks which are stored as individual documents in two collections:

 1. `chunk collection` - stores the document part. Each chunk is limited to 255 KB in size. 

 2. `file collection` - stores the consequent additional metadata. When reading from GridFS, the driver re-assembles all the chunks as needed. It makes it easier to read a section of a file as per our query range.

<p align="center">
 <img height=400 width=800 src="https://user-images.githubusercontent.com/97250268/197802102-719221c1-005b-4dc1-bce2-ba0cce61830d.png">
</p>

### Installing MongoDB Community Edition

- In the terminal - use the command: `wget -qO - https://www.mongodb.org/static/pgp/server-4.2.asc | sudo apt-key add -`
- Create a list file for MongoDB:
```
 echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu bionic/mongodb-org/4.2 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.2.list
```
- Command to reload the local package database `sudo apt-get update`
- Install the specific version  of MongoDB
```
sudo apt-get install -y mongodb-org=4.2.18 mongodb-org-server=4.2.18 mongodb-org-shell=4.2.18 mongodb-org-mongos=4.2.18 mongodb-org-tools=4.2.18
```
- To start the mongoDB `sudo systemctl start mongod`

### Creating Database in mongoDB:

- Step 1: To access the mongodb shell - use `mongo` command.

- Step 2: To check for existing databases - use `show dbs1` command.
    
- Step 3: To create the database - use `use [database_name]` command. For e.g. `use teams_app`
  
- Step 4: To create a `collection` called `video_storage` - `db.createCollection(“video_storage”)`

### How to store Huge Media Files in Mongo Database:

- Give the command `mongofiles -d [Name of the database] put "path of the videofile"`
- mongofiles -d teams_app put "path of the videofile"
- 

-

# Entity Relationship Diagram (ERD)

Also known as Entity Relationship model, ERD is a graphical representation that shows the relationships between different entity or tables in the database. It shows what kind of relation they have like `1 to 1` or `1 to many`.

In our app, In the *first iteration* we have 4 different Tables

1. user - To store the user login details.
2. user_details - To store the user personal details.
3. session_details - To store the sessions logs of the user.
4. call_log - To store the call, made by the users.

The relations between the tables can be classified as follows:

1. user & user_details will have `1 to 1 mandatory` relation.
2. user & session_details will have `1 to many` relation.
3. sessions_details and call_log will have `1 mandatory to many optional` relation.


- The following `ER Diagram` shows the above relation between the tables.

<p align="center">
    <img src="https://user-images.githubusercontent.com/110366380/197568046-6b724064-5e66-49ce-9c69-0db6b3775585.jpg">
</p>




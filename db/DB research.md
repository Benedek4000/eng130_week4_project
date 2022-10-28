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
    - `sudo systemctl enable ssh`
    - `sudo systemctl restart ssh`
    - we should now be able to connect to our vm using ssh
    - to connect to vm with filezilla
      - use sftp server
      - host: 127.0.0.1
      - user: sftp_user
      - password: sftp_user
      - port: 22


## Hosting server on Linux with Vagrant

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

### Creating a `Vagrantfile` to for the Virtual Machine where the database will run

- The following script is for the vagrant file, which uses ip address `192.168.10.150`

```
Vagrant.configure("2") do |config|
    config.vm.box = "ubuntu/bionic64"
    config.vm.network "private_network", ip: "192.168.10.150", type: "dhcp"
    config.vm.network "forwarded_port", guest: 27017, host: 80 
       auto_correct: true
    config.vm.provision "shell",path: "provision.sh"
end
```
- For Automation, the `provision.sh` file includes all the required commands to install and run `mongodb`. We use `wget` to retrieve contents from web server. We also install `apache server`

```
# To Update the system & then Upgrade it
sudo apt-get update -y
sudo apt-get upgrade -y

# Install MongoDB

# Retrieve the mongodb insallation files from the server using wget
wget -qO - https://www.mongodb.org/static/pgp/server-4.2.asc | sudo apt-key add -

# Create a list file for MongoDB
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu bionic/mongodb-org/4.2 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.2.list

# Reload the local package database
sudo apt-get update

# Installing the specific version of MongoDB
sudo apt-get install -y mongodb-org=4.2.18 mongodb-org-server=4.2.18 mongodb-org-shell=4.2.18 mongodb-org-mongos=4.2.18 mongodb-org-tools=4.2.18

# Starting the mongod process & enabling it
sudo systemctl start mongod
sudo systemctl enable --now mongod 

# Installing the Apache Server
sudo apt install apache2 -y

# Connect to localhost and port 80
curl -v localhost:80
```
### Creating Database in mongoDB

- Step 1: To access the mongodb shell - use `mongo` command.

- Step 2: To check for existing databases - use `show dbs` command.

- Step 3: To create the database - use `use [database_name]` command. For e.g. `use teams_app`
  
- Step 4: To create a `collection` called `video_storage` - `db.createCollection(“video_storage”)`

### How to store Huge Media Files in Mongo Database

- To store the files: Use the command `mongofiles -d [Name of the database] put "path of the videofile"` Example:

- `mongofiles -d teams_app put "<path of the file>"`

To retrieve the file:
- `mongofiles -d teams_app get "<name of the file>"`
  
- Go inside the database: `use <name of the database>`
  
- we have 2 files: `fs.files` and `fs.chuncks`
- To see the whole files `db.fs.files.find().pretty()`
- To see the chuncks `db.fs.chuncks.find({},{data:0,_id:0}).pretty()`  
  
```
- Work under progress
```

## Normalisation

Normalization is the process of organizing the data in the database. It is used to minimize the redundancy from the database, so that we can eliminate undesirable characteristics like Insertion, Update and Deletion anomalies.

- A normalisation typically divides the larger table into smaller table and links them using relationships.
- The normal form is used to reduce redundancy from the database table.

We need a database to be atleast normalised to Third Normal Form `3NF` to achieve this.

### First Normal Form

- The data must be atomic.
- There should be no repeated groups.
- Each row must be unique.

### Second Normal Form

- Already in First Normal Form `1NF`.
- All non-key attributes must functionally depend upon the full primary key.

### Third Normal Form

- Already in the Second Normal Form `2NF`.
- There are no transitive dependencies.

## Entity Relationship Diagram (ERD)

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

In the *Second Iteration*, we decided to reduce the number of table to 2.

- The `user` & `user_details` table have lot of fields, which are redundent for the initial app. We merge those 2 tables in one.

- Instead of having multiple logs for the same session, we have decided to keep it simple by storing each session as whole.

The updated `ER Diagram` is much clear and simplified.

<p align="center">
    <img src="https://user-images.githubusercontent.com/110366380/198003869-7edf9b53-ca34-4293-a964-93c4740c418f.png">
</p>

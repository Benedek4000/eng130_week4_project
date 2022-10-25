# Database

- We will use SQL to query for data
  - Flat file database for recordings
    - No repetitions anyway due to location, time stamps
  - Relational database to store user information
- We will use (most likely) MongoDB for both databases
  - We have used it and linked it before so will be relatively easy to do

## Relational database choice

We will use PostgreSQL for the relational database as it offers a lot of features like SQL querying, API support, migration to bigger databases and is supported on many operating systems

`https://db-engines.com/en/system/PostgreSQL`
![comparison](images/mysql_vs_postgresql.png)

We could have also chosen MySQL to create our relational database for the users but we decided on PostgreSQL as it is becoming more popular due to its API support.

### Setting up PostgreSQL

Set up in a virtual machine which will host the database.

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

# DB

### What is MongoDB?

- It is a NoSQL database called (Document database)

- It stores data in flexible JSON - like document

- It is higly scalable and flexible database.

### How MongoDB looks when compared to RDBMS

- In RDBMS the data is stored in tables, whereas in MONGODB the data is stored in JSON format.

### The Structure of MongoDB database

- MongoDB physical daatbase contain several logical databases.

- Each database contain several collections. Collection is something like table in relational database.

- Each collection contains several documents. Document is something like record or row in RDBMS.

### Key Characteristics of MongoDB database

- Installation and setup is very easy

- All information related to a document is stored in a single place.

-

-

# DB

### What is MongoDB?

- It is a NoSQL database called (Document database)

- It stores data in flexible JSON - like document

- It is higly scalable and flexible database.

### How MongoDB looks when compared to RDBMS

- In RDBMS the data is stored in tables, whereas in MONGODB the data is stored in JSON format.

### The Structure of MongoDB database

- MongoDB physical daatbase contain several logical databases.

- Each database contain several collections. Collection is something like table in relational database.

- Each collection contains several documents. Document is something like record or row in RDBMS.

### Key Characteristics of MongoDB database

- Installation and setup is very easy

- All information related to a document is stored in a single place.

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

Picture for ERD

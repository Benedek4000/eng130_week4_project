# How to setup and run the VMs with databases

## Creation of VMs

1. Open git bash and navigate to the VMs folder
2. Run `vagrant up postgresql && vagrant ssh postgresql` - this will create the PostgreSQL database
3. Open a seperate git bash terminal and navigate to VMs folder again
4. Run `vagrant up mongodb && vagrant ssh mongodb`

## MongoDB

The VM will be created and most necessary commands will already be run.
The remaining ones are below.
i.e. once the MongoDB VM is created, run the following commands to create the actual database.

### Creating Database in mongoDB

1. To access the mongodb shell - use `mongo` command.
2. To check for existing databases - use `show dbs` command.
3. To create the database - use `use [database_name]` command. For e.g. `use teams_app`
4. To create a `collection` called `video_storage` - `db.createCollection(“video_storage”)`
5. To insert into a table/collection
6. ```
   db.collection.insert(
        <document or array of documents>,
        {
            writeConcern: <document>,
            ordered: <boolean>
        }
    )
    ```
    Example: `db.video_storage.insert( { item: "card", qty: 15 } )`

7. To print contents of table - `db.products.find().pretty()`, prints them in a dictionary format for ease of use



## PostgreSQL

### Creating Database in PostgreSQL

The VM will be created with the vagrant commands.
All you need to now do is to enter the postgresql interface and run a premade script to create the database and tables you need.

1. `sudo -u postgres psql` - will enter the interface
2. Set a password - `\password`
3. Type the password (e.g. `spartaglobal`)
4. It might appear as if nothing is happening when you type but that is the way terminal censors password entering, i.e. you are typing. Do not worry though, you will have to enter the password again.
5. Once in there, type `CREATE DATABASE users;`
6. Enter the database, `\c users`
7. Create tables, `\i /home/vagrant/sync/sqlscripts/create_users_tables.sql`
8. Ensure everything is made correctly, `SELECT * FROM users;`
9. You should see an empty table
10. Details about ports and IP required are in Vagrantfile (port: `22`, ip: `192.168.10.149`)
11. Details of tables/database:
   1. Name: `postgres`
   2. Password: `spartaglobal` , or whatever you set in step 2
   3. Table names
      1. `users` - stores user details (email, password(hashed), name, etc.)
      2. `sessions` - stores recording session details (date, time, location)

## Maintenence 

- Please ensure you include `.vagrant` folder in your `.gitignore` as it is a big folder.
- Likewise for the virtual machine console log files, e.g. `ubuntu-bionic-18.04-cloudimg-console.log`
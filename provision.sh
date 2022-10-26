# update system
sudo apt-get update -y
# upgrade system
sudo apt-get upgrade -y

# Install MongoDb
# Steps to Install MongoDB Community Edition 
wget -qO - https://www.mongodb.org/static/pgp/server-4.2.asc | sudo apt-key add -
# Create a list file for MongoDB using the below command
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu bionic/mongodb-org/4.2 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.2.list
# Command to reload the local package database
sudo apt-get update
# Install the specific version  of MongoDB
sudo apt-get install -y mongodb-org=4.2.18 mongodb-org-server=4.2.18 mongodb-org-shell=4.2.18 mongodb-org-mongos=4.2.18 mongodb-org-tools=4.2.18
# You can start the mongod process by issuing the following command
sudo systemctl start mongod

# Steps to install apache server in the virtual machine
# Before we install Apache we should do package update
sudo apt update
# Now let's install Apache
sudo apt install apache2 -y
# We will connect to localhost and port 80
curl -v localhost:80

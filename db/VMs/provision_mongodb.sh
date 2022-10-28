sudo apt-get update
sudo apt-get upgrade -y
curl -fsSL https://www.mongodb.org/static/pgp/server-4.4.asc | sudo apt-key add -
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/4.4 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.4.list
sudo apt update
sudo apt install mongodb-org -y
sudo apt install net-tools -y
rm /etc/mongod.conf
cp /home/vagrant/sync/mongod.conf /etc/mongod.conf
sudo systemctl start mongod.service
sudo systemctl enable mongod

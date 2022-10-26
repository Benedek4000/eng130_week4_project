sudo apt-get update
sudo apt-get upgrade -y
sudo apt install wget ca-certificates -y
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ $(lsb_release -cs)-pgdg main" >> /etc/apt/sources.list.d/pgdg.list'
sudo apt update
sudo apt install postgresql postgresql-contrib -y
sudo rm /etc/postgresql/15/main/postgresql.conf /etc/postgresql/15/main/pg_hba.conf
cp /home/vagrant/sync/postgresql.conf /etc/postgresql/15/main/postgresql.conf
cp /home/vagrant/sync/pg_hba.conf /etc/postgresql/15/main/pg_hba.conf
sudo service postgresql status
sudo apt install apache2 -y
sudo systemctl status apache2
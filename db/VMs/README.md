
- run virtual machine
- type the following commands:
```commandline
sudo -u postgres psql
\password
[FOLLOW INSTRUCTIONS]
CREATE DATABASE users;
\c users
\i /home/vagrant/sync/sqlscripts/create_users_tables.sql
SELECT * FROM users;
```
# Back-end for the project

> Developed in a virtual environment for python3

## Deployment

### Requirements

1. python3,pip

2. flask module(pip install flask)

3. mysql(sudo apt-get install mysql-server libmysqlclient-dev)(pip install flask-mysqldb)(pip install Flask-WTF)(pip install passlib)

4. required python libraries

basic structure of database is given below

In a python environment(new),
requirements.txt contains the packages and modules needed in python venv, just run the command in your environment

```sh
source /path/to/venvfolder/bin/activate
pip install -r requirements.txt
```

use the following command to run the project:

```sh
flask run --host=0.0.0.0 --port=12345
or
python app.py
```

### Sql initialization (mysql -server)

1. set up the database in mysql server
    1. create database pragyan_hack;
    2. use pragyan_hack;
    3. create table users(user_id int(11) auto_increment primary key,name varchar(100),email varchar(100),username varchar(30),password varchar(100),register_date timestamp default current_timestamp);
    4. create table situations (situation_id int(11) auto_increment primary key, user_id int(11), situation_date );
    5. create table entries (entry_id int(11) auto_increment primary key,user_id int(11),title varchar(255),msg text , situation_date timestamp default current_timestamp ,appentry_date timestamp);

2. create a new user in mysql localhost
    1. mysql -u root -p
    2. create user 'pragyan_hack'@'localhost' identified by 'Pragyan_hack123';
    3. GRANT ALL PRIVILEGES ON pragyan_hack.* TO 'pragyan_hack'@'localhost';
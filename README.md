# ChatRooms

!(abifog-chatrooms)['/screenshots/abifog-chatrooms.png']

## Stack
* Flask
* PostgresSQL - store the entire database url (local or remote)  in an environment variable called DATABASE_URL
* Websockets
* HTML/CSS/JS

## Features
* multi user chatrooms
* ability to create channels
* user authentication
* remembers your last used channels\

## Setup

* setup a virtualenv and install requirements.txt
* `export DATABASE_URL=postgres://link.to.your.url.com/whatever`
* run create_db.py to create your tables
* `flask run` to run it in a developement setting. 

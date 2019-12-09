### Initialization

#### 1. Python Virtual Environment
For Windows User
- run command prompt
- type `pip install virtualenv`

Creating a virtualenv
- go to server folder
- type `virtualenv .pyenv`

To activate the isolated virtualenv  
If you are using `powershell` or `powershell-based` VSCode terminal
- go to server folder
- run `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` once
- run `.\\.pyenv\Scripts\activate`

If you are using `command prompt`
- go to server folder
- run `.\\.pyenv\Scripts\activate`

Installing Python Dependencies in the Environment
- go to server folder
- run `python -m pip install -r requirements.txt`

#### 2. Using Virtual Environment
Installing new dependencies
- run `python -m pip install xxx`
- update requirements.txt with the right version

#### 3. Use .env
- Create .env file in server folder
- Add in the following:

 Change values according to your local machine
```
SQL_DB=isit_database
SQL_HOST=18.139.175.98
SQL_USER=root
SQL_PW=password

MONGO_HOST=3.134.250.90
MONGO_DB=isit_database_mongo
LOG_DB=log_mongo
```

#### 4. Development
Project Structure
server  
| .pyenv `(contains python dependencies for this project)`  
| common `(contains all the connectors to the Dbs and some shared function)`  
|-| util.py `(utilities function such as connectors)`  
|-| env.py  
| resources `(contains more specific functions)`  
|-| book_preview.py  
|-| categories.py  
|-| logs.py  
|-| metadata.py  
|-| review.py  
|-| test.py  
|-| user.py  
| app.py `(contains all the route and endpoints)`  
| README.md  
| requirements.txt

Running the web app
- run `python app.py`

Create a new resource
- go to ./resources
- create a new .py file
```python
from flask import json
from flask_restful import Resource
class Foo(Resource):
    def get(self):
        return 'hello world'
```

Create new endpoint
- Follow Create a new resource tutorial
- go to `app.py`
- add new import `from resource.foo import Foo`
- add new resource in this syntax api.add_resource(<Function name>, <endpoint>) e.g. `api.add_resource(Foo, '/foo')` (running `localhost:5000/foo` will call the GET function from function Foo)

#### 5. PyMongo
- Install mongodb server community edition from [here](https://www.mongodb.com/download-center/community)
- create a new database called `isit_database_mongo`
- make sure mongo server is running on port:27017
- run `mongod` in any shell
- create an admin user with username: `isit_database_mongo` password: `password`

for the API, go [here](https://docs.mongodb.com/manual/reference/method/)
To GET data from the database
- import `from common.util import mongo`
- use the syntax: `mongo.db.<collection name>.<mongo function>` e.g. `mongo.db.logs.find({})

#### 6. MySQL
- Install MySQL server version 5.7.27 from [here](https://dev.mysql.com/downloads/windows/installer/5.7.html)
- Create the followint table in existing database:
```
CREATE TABLE IF NOT EXISTS `kindle_reviews` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `asin` VARCHAR(255) NOT NULL,
  `helpful` VARCHAR(255) NOT NULL,
  `overall` INT(11) NOT NULL,
  `reviewText` TEXT NOT NULL,
  `reviewTime` VARCHAR(255) NOT NULL,
  `reviewerID` VARCHAR(255) NOT NULL,
  `reviewerName` VARCHAR(255) NOT NULL,
  `summary` VARCHAR(255) NOT NULL,
  `unixReviewTime` INT(11) NOT NULL,
  PRIMARY KEY (`id`));

```
- To load dataset:
```
SET sql_mode='NO_AUTO_VALUE_ON_ZERO';

LOAD DATA LOCAL INFILE 'C:\\ProgramData\\MySQL\\MySQL Server 5.7\\Data\\kindle_reviews.csv' 
INTO TABLE kindle_reviews
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

```

#### 7. JWT User Login
Update local `isit_database_mongo` mongodb with a new collection called `user_login`.

Sign up workflow  
- Requires username, password and name. Username must be unique
- Check whether fields are filled
- Check whether username already exists
- Create a unique secret for the user to encode the username and password with jwt

Login workflow
- Requires username and password
- Check whether fields are filled
- Check whether username is in the collection
- Getting the user secret and reencode the entered password with the secret to see if the result match
- Will return the jwt token if successful

#### 8. Categories
- Create a new collection under `isit_database` db named `categories` and download and import 
[categories.json](https://sutdapac-my.sharepoint.com/:f:/g/personal/andre_hadianto_mymail_sutd_edu_sg/Ev8VGVvdq4tMoNijJmy7oSkBE0G-PDxe13UgN70wbY8E5A?e=1CNZZB) to the collection.
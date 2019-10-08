### Initialization

#### 1. Python Virtual Environment
For Windows User
- run command prompt
- type `pip install virtualenv`

Creating a virtualenv
- go to project root folder
- type `virtualenv .pyenv`

To activate the isolated virtualenv  
If you are using powershell or powershell-based VSCode terminal
- go to root folder
- run `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` once
- run `.\\.pyenv\Scripts\activate`

If you are using command prompt
- go to root folder
- run `.\\.pyenv\Scripts\activate`

Installing Python Dependencies
- go to root folder
- run `python -m pip install -r requirements.txt`

#### 2. Using Virtual Environment
Installing new dependencies
- run `python -m pip install xxx`
- update requirements.txt with the right version

#### 3. Development
Project Structure
root  
| common `(contains all the connectors to the Dbs and some shared function)`  
|-| util.py `(utilities function such as connectors)`  
| resources `(contains more specific functions)`  
|-| `(insert function)`  
| app.py `(contains all the route and endpoints)`    

Running Flask
- run `python -m flask run --reload`

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

#### 4. PyMongo
- Install mongodb server community edition from [here](https://www.mongodb.com/download-center/community)
- create a new database called `isit_database_mongo`
- make sure mongo server is running on port:27017
- run `mongod` in any shell
- create an admin user with username: isit_database_mongo password: password

for the API, go [here](https://docs.mongodb.com/manual/reference/method/)
To GET data from the database
- import `from common.util import mongo`
- use the syntax: `mongo.db.<collection name>.<mongo function>` e.g. `mongo.db.logs.find({})





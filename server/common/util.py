import os
from flask import Flask
from flask_pymongo import PyMongo
from common.env import getenv
import mysql.connector as db

# Get environment variables from .env
getenv()

SQL_DATABASE = os.getenv("SQL_DB")
SQL_HOST = os.getenv("SQL_HOST")
SQL_USER = os.getenv("SQL_USER")
SQL_PW = os.getenv("SQL_PW")

# Connect to mongodb
MONGO_DB = os.getenv("MONGO_DB")
app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/{}".format(MONGO_DB)
mongo = PyMongo(app)

# Connect to MySQL
con = db.connect(host=SQL_HOST, user=SQL_USER, passwd=SQL_PW, db=SQL_DATABASE)
cursor = con.cursor()
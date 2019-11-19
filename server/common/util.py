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
MONGO_HOST = os.getenv("MONGO_HOST")
MONGO_DB = os.getenv("MONGO_DB")
LOG_DB = os.getenv("LOG_DB")
app = Flask(__name__)
# kindle metadata
mongo = PyMongo(app, uri="mongodb://admin:password@{}:27017/{}?authSource=admin".format(MONGO_HOST, MONGO_DB))
# logs
mongo_log = PyMongo(app, uri="mongodb://admin:password@{}:27017/{}?authSource=admin".format(MONGO_HOST, LOG_DB))

# Connect to MySQL
def connect():
    con = db.connect(host=SQL_HOST, user=SQL_USER, passwd=SQL_PW, db=SQL_DATABASE)
    cursor = con.cursor()
    return con, cursor
    
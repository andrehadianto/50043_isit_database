from flask import Flask
from flask_pymongo import PyMongo
import mysql.connector as db

DATABASE = "isit_database"
HOST = "localhost"

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/isit_database_mongo"
mongo = PyMongo(app)

con = db.connect(host=HOST, user="root", passwd="root", db=DATABASE)
cursor = con.cursor()
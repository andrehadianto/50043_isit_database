from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/isit_database_mongo"
app.config['LOG_MONGO'] = "mongodb://localhost:27017/log_mongo"
mongo = PyMongo(app)
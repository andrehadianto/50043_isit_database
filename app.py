from flask import Flask
from flask_restful import Api
from resources.foo import testMongo, testMySql
import common.util

app = Flask(__name__)
api = Api(app)

api.add_resource(testMySql, '/mysql')
api.add_resource(testMongo, '/mongo')
    
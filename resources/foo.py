from flask import json
from flask_restful import Resource
from common.util import mongo

class Foo(Resource):
    def get(self):
        text = mongo.db.logs.find_one({"complaint": "Why are you gay"})["complaint"]
        return text
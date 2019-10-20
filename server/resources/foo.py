from flask import render_template, make_response, json
from flask_restful import Resource
from common.util import mongo, connect

from bson import json_util
import json

class testMongo(Resource):
    def get(self):
        obj = mongo.db.kindle_metadata.find_one({"asin": "B000MAHACE"})
        return json.dumps(obj, default=json_util.default)

class testMySql(Resource):
    def get(self):
        con, cursor = connect()
        cursor.execute("describe kindle_reviews")
        res = cursor.fetchall()
        con.close()
        return res
        
class Foo(Resource):
    def get(self):
        headers = {'Content-type': 'text/html'}
        return make_response(render_template("index.html"),200,headers)

from flask import render_template, make_response
from flask_restful import Resource, reqparse
from flask_restful import Resource
from common.util import mongo, cursor

from bson.json_util import dumps
from bson import json_util
import json

class BooksListResource(Resource):
    """Returns books information (lightweight) with pagination"""
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('page', type=int, location='args')
        parser.add_argument('count', type=int, location='args')
        args = parser.parse_args()
        
        _limit = args['count']
        _offset = (args['page']-1) * args['count']
        
        # Returns only fields asin and imUrl
        cursor = mongo.db.kindle_meta.find({},
             {"asin" : 1, "imUrl" : 1}).skip(_offset).limit(_limit)
        jsonstring = json_util.dumps(cursor, default=json_util.default)
        return json.loads(jsonstring)
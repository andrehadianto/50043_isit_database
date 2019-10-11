from flask import request
from flask_restful import Resource, reqparse
from common.util import mongo, cursor

from bson.json_util import dumps, default
import json

class BooksListResource(Resource):
    """Returns books information (lightweight) with pagination"""
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('page', type=int, location='args')
        parser.add_argument('count', type=int, location='args')
        args = parser.parse_args()

        if (not args['count'] or not args['page']):
            cursor = mongo.db.kindle_meta.find({},
                {"asin" : 1, "imUrl" : 1, "title" : 1}).skip(0).limit(15)
            jsonstring = dumps(cursor, default=default)
            return json.loads(jsonstring)
        
        _limit = args['count']
        _offset = (args['page']-1) * args['count']
        cursor = mongo.db.kindle_meta.find({},
             {"asin" : 1, "imUrl" : 1}).skip(_offset).limit(_limit)
        jsonstring = dumps(cursor, default=default)
        return json.loads(jsonstring)

class UpdateBookResource(Resource):
    def get_filled_fields(self, field_names, fields):
        """Returns a dictionary of fields that were updated"""
        to_be_updated = {}
        for field_name, field in zip(field_names, fields):
            if field != None:
                to_be_updated[field_name] = field
        return to_be_updated

    def put(self, asin):
        """Updates book details
            Parameters: asin
            Body: json(title, categories, imUrl, related?, price?, description)
            """
        parser = reqparse.RequestParser()
        parser.add_argument('title', type=str, location='form')
        # parser.add_argument('categories', location='form')
        parser.add_argument('imUrl', type=str, location='form')
        # parser.add_argument('related', location='form')
        parser.add_argument('price', type=float, location='form')
        parser.add_argument('description', type=str, location='form')
        args = parser.parse_args()

        _title = args.get('title')
        _imUrl = args.get('imUrl')
        _price = args.get('price')
        _description = args.get('description')

        field_names = ['title', 'imUrl', 'price', 'description']
        fields = [_title, _imUrl, _price, _description]
        to_be_updated = self.get_filled_fields(field_names, fields)

        try:
            cursor = mongo.db.kindle_meta.update({"asin": asin}, {"$set": to_be_updated})
            if cursor['updatedExisting']:
                return {"message": "Book details updated", "body": to_be_updated}, 200
            raise Exception("Something went wrong during book update to Database")
            
        except Exception as e:
            print(e)
            return {"message": "Server Error"}, 500



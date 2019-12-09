from flask import json
from flask_restful import Resource, request, reqparse
from common.util import mongo
from bson.json_util import dumps, default
from random import random

class GetBookTitles(Resource):
    """Returns all book titles"""
    def get(self):
        try:
            cursor = mongo.db.kindle_metadata.find({'title': {'$exists': 1}}, {'title': 1})
            json_query = json.loads(dumps(cursor, default=default))
            return {"message": "Successfully retrieve all titles", "titles": json_query}, 200
        except:
            return {"message": "Failed to retrieve all titles"}, 500

class GetBookDetails(Resource):
    """Returns book details (all available fields)"""
    def get(self, asin):
        cursor = mongo.db.kindle_metadata.find_one({'asin': asin})
        jsonstring = dumps(cursor, default=default)
        return json.loads(jsonstring)

class BooksListResource(Resource):
    """Returns books information (lightweight) with pagination"""
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('page', type=int, location='args')
        parser.add_argument('count', type=int, location='args')
        args = parser.parse_args()

        _total_count = mongo.db.kindle_metadata.count()

        if (not args['count'] or not args['page']):
            cursor = mongo.db.kindle_metadata.find({},
                {"asin" : 1, "imUrl" : 1, "title" : 1}).skip(0).limit(15)
            json_query = json.loads(dumps(cursor, default=default))
            return {"message": "Successfully retrieve all books", "books": json_query, "count": _total_count}, 200
        
        _limit = args['count']
        _offset = (args['page']-1) * args['count']
        cursor = mongo.db.kindle_metadata.find({},
             {"asin" : 1, "imUrl" : 1}).skip(_offset).limit(_limit)
        json_query = json.loads(dumps(cursor, default=default))
        return {"message": "Successfully retrieve all books", "books": json_query, "count": _total_count}, 200

class RegisterNewBook(Resource):
    def get_filled_fields(self, field_names, fields):
        """helper function"""
        to_be_updated = {}
        for field_name, field in zip(field_names, fields):
            if field != None:
                to_be_updated[field_name] = field
        return to_be_updated

    def generate_padded_number(self):
        random_int = int(random() * 10000000000)
        int2str = str(random_int)
        return int2str.zfill(10)

    def post(self):
        """Returns a dictionary of fields that were updated"""
        req_json = request.get_json(force=True)

        try: 
            _title = req_json['title']
            _imUrl = req_json['imUrl']
            _description = req_json['description']
        except Exception as e:
            print(e)
            return {"message": "title, imUrl and description are required fields"}, 400

        _price = round(float(req_json.get('price')),2)
        _categories = req_json.get('categories')
        _related = req_json.get('related')
        _asin = self.generate_padded_number()

        field_names = ['asin', 'title', 'imUrl', 'description', 'price', 'categories', 'description', 'related']
        fields = [_asin, _title, _imUrl, _description, _price, [_categories], _description, _related]
        query = self.get_filled_fields(field_names, fields)
        try:
            mongo.db.kindle_metadata.insert_one(query)
            return {"message": "Book registered", "body": json.loads(dumps(query))}, 200
            
        except Exception as e:
            print(e)
            return {"message": "Server Error"}, 500

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
        json_request = request.get_json(force=True)
        _title = json_request.get('title')
        _imUrl = json_request.get('imUrl')
        _categories = json_request.get('categories')
        _price = json_request.get('price')
        _description = json_request.get('description')

        field_names = ['title', 'imUrl', 'categories','price', 'description']
        fields = [_title, _imUrl, _categories, _price, _description]
        to_be_updated = self.get_filled_fields(field_names, fields)

        try:
            cursor = mongo.db.kindle_metadata.update({"asin": asin}, {"$set": to_be_updated})
            if cursor['updatedExisting']:
                # return the updated book if update was successful
                cursor = mongo.db.kindle_metadata.find_one({"asin": asin})
                jsonstring = dumps(cursor, default=default)
                updated_json_body = json.loads(jsonstring)
                return {"message": "Book details updated", "body": updated_json_body}, 200
            raise Exception("Something went wrong during book update to Database")
            
        except Exception as e:
            print(e)
            return {"message": "Server Error"}, 500

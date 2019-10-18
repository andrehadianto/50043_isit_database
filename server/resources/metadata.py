from flask import json
from flask_restful import Resource, request, reqparse
from common.util import mongo
from bson.json_util import dumps, default

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

        if (not args['count'] or not args['page']):
            cursor = mongo.db.kindle_metadata.find({},
                {"asin" : 1, "imUrl" : 1, "title" : 1}).skip(0).limit(15)
            jsonstring = dumps(cursor, default=default)
            return json.loads(jsonstring)
        
        _limit = args['count']
        _offset = (args['page']-1) * args['count']
        cursor = mongo.db.kindle_metadata.find({},
             {"asin" : 1, "imUrl" : 1}).skip(_offset).limit(_limit)
        jsonstring = dumps(cursor, default=default)
        return json.loads(jsonstring)

class RegisterNewBook(Resource):
    def get_filled_fields(self, field_names, fields):
        "helper function"
        to_be_updated = {}
        for field_name, field in zip(field_names, fields):
            if field != None:
                to_be_updated[field_name] = field
        return to_be_updated

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
        #TODO: implement checker for imUrl 

        _price = req_json.get('price')
        _categories = req_json.get('categories')
        _related = req_json.get('related')
        
        field_names = ['title', 'imUrl', 'description', 'price', 'description', 'related']
        fields = [_title, _imUrl, _description, _price, _description, _related]
        to_be_updated = self.get_filled_fields(field_names, fields)

        try:
            cursor = mongo.db.kindle_metadata.insert({"asin": 'B000000000'}, {"$set": to_be_updated})
            #TODO: generate asin dynamically
            return {"message": "Book registered", "insertedId": str(cursor), "body": to_be_updated}, 200
            
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

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



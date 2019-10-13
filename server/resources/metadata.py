from flask import json
from flask_restful import Resource, request, reqparse
from common.util import mongo
from bson.json_util import dumps, default

#get book by id or asin via query param
class GetBookDetails(Resource):
    """Returns book details (all available fields)"""
    def get(self, asin):
        cursor = mongo.db.kindle_metadata.find_one({'asin': asin})
        jsonstring = dumps(cursor, default=default)
        return json.loads(jsonstring)

class RegisterNewBook(Resource):
    def get_filled_fields(self, field_names, fields):
        """Returns a dictionary of fields that were updated"""
        to_be_updated = {}
        for field_name, field in zip(field_names, fields):
            if field != None:
                to_be_updated[field_name] = field
        return to_be_updated

    def post(self):
        json = request.get_json(force=True)
        _title = json['title']
        _imUrl = json['imUrl']
        _price = json['price']
        _description = json['description']
        
        field_names = ['title', 'imUrl', 'price', 'description']
        fields = [_title, _imUrl, _price, _description]
        to_be_updated = self.get_filled_fields(field_names, fields)

        try:
            cursor = mongo.db.kindle_metadata.insert({"asin": 'B000000000'}, {"$set": to_be_updated})
            return {"message": "Book registered", "insertedId": str(cursor), "body": to_be_updated}, 200
            
        except Exception as e:
            print(e)
            return {"message": "Server Error"}, 500



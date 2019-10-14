from flask import render_template, make_response
from flask import request
from flask_restful import Resource, reqparse
from flask_restful import Resource
from common.util import mongo, cursor

from bson.json_util import dumps
from bson import json_util
import json

class MetaAPI(Resource):
    """Returns books information (lightweight) with pagination"""
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('page', type=int, location='args')
        parser.add_argument('count', type=int, location='args')
        args = parser.parse_args()
        
        _limit = args['count']
        _offset = (args['page']-1) * args['count']
        
        # Returns only fields asin and imUrl
        cursor = mongo.db.kindle_metadata.find({},
             {"asin" : 1, "imUrl" : 1}).skip(_offset).limit(_limit)
        jsonstring = json_util.dumps(cursor, default=json_util.default)
        return json.loads(jsonstring)


class BookPreviewResource(Resource):
    
    def post(self):
        """Returns book information (lightweight) """
        # asinArray: array of string
        # Response Body: Array of json(asin, title, imURL?)
        parser = reqparse.RequestParser()
        parser.add_argument('asinArray', type=str, location='form')
        args = parser.parse_args()
        asinArray = args.get('value')
        print(asinArray)

        #print(cursor)
        #print("jsonString:",jsonstring)
        #check if bookInfoInJSON is empty?
        #bookInfoInJSON.append(booksJSONArray)
          
        #print("BOOKS JSON ARRAY: ", booksJSONArray)
        #return booksJSONArray
        # create an array to host the json
        # For each asin in asinArray, parse and request for the asin and its relevant info
        # If don't exist, put some placeholder
        # host each asin and its info into the array as a json
        # 

class BookCategoryResource(Resource):
    
    def post(self, categoryArray):
        # categoryArray: array of string
        # Response Body: array of json(asin, title, imUrl?)
        # create empty array
        # get response for categoryArray[0]
        # from responses for categoryArray[0], check if the response has the remaining categories
        # if have, put in empty array, else dispose
        parser = reqparse.RequestParser()
from flask import render_template, make_response
from flask import request
from flask_restful import Resource, reqparse
from flask_restful import Resource
from common.util import mongo, cursor


from bson.json_util import dumps
from bson import json_util
import json

class BookPreviewResource(Resource):
    
    def post(self):
        """Returns book information (lightweight) """
        # asinArray: array of string
        # Response Body: Array of json(asin, title, imURL?)
        parser = reqparse.RequestParser()
        parser.add_argument('asinArray', type=str, location='form')
        args = parser.parse_args()
        asinArray = args.get('asinArray').split(",")
        print(asinArray)
        # create an array to host the json
        booksJSONArray = list()
        
            # For each asin in asinArray, parse and request for the asin and its relevant info
        for asin in asinArray:
            bookInfo = mongo.db.isit_database.find_one({"asin":asin})
            print("bookInfo:" ,bookInfo)

            book_asin = asin
            
            try:
                book_title = bookInfo["title"]
            except Exception as e:
                book_title = "untitled"
                
            try:
                book_imUrl = bookInfo["imUrl"]
            except Exception as e:
                book_imUrl = bookInfo[""]
              
            bookLW = {"asin": book_asin, "title": book_title, "imUrl":book_imUrl}
            booksJSONArray.append(json.dumps(bookLW))
        
        return booksJSONArray


    

class BookCategoryResource(Resource):
    
    def post(self, categoryArray):
        # categoryArray: array of string
        # Response Body: array of json(asin, title, imUrl?)
        # create empty array
        # get response for categoryArray[0]
        # from responses for categoryArray[0], check if the response has the remaining categories
        # if have, put in empty array, else dispose
        parser = reqparse.RequestParser()
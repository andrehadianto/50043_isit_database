from flask import render_template, make_response, request
from flask_restful import Resource, reqparse
from common.util import mongo, cursor


from bson.json_util import dumps
from bson.son import SON
from bson import json_util
import json

default_book_title = "untitled"
default_img_Url = "no-url"
# mongodb_database = kindle_metadata

class BookPreviewResource(Resource):
    
    def post(self):
        """Returns book information (lightweight)   
        Request Body: (asinArray) Array of string 
        Response Body: Array of json(asin,title,imUrl)"""

        # asinArray: array of string
        # Response Body: Array of json(asin, title, imURL?)
        json_request = request.get_json(force=True)
        _asinArray = json_request.get('asinArray')
        # create an array to host the json
        booksJSONArray = list()
        
            # For each asin in asinArray, parse and request for the asin and its relevant info
        for asin in _asinArray:
            bookInfo = mongo.db.kindle_metadata.find_one({"asin":asin})
            book_asin = asin
            
            try:
                book_title = bookInfo["title"]
            except Exception as e:
                book_title = default_book_title 
                
            try:
                book_imUrl = bookInfo["imUrl"]
            except Exception as e:
                book_imUrl = default_img_Url
              
            bookLW = {"asin": book_asin, "title": book_title, "imUrl":book_imUrl}
            booksJSONArray.append(json.dumps(bookLW))
        
        return booksJSONArray


    

class BookCategoryResource(Resource):
    
    def post(self):

        """Returns books that have categories containing categories in categoryArray
        Request Body: (categoryArray) Array of String 
        Response Body: Array of json(asin, title, imUrl)"""
        json_request = request.get_json(force=True)
        _categoryArray = json_request.get('categoryArray')
        filteredArray = list()
        for item in mongo.db.kindle_metadata.find():
            counter = 0
            for category in _categoryArray:
                if category in list(item["categories"]):
                    counter += 1
            if counter == len(_categoryArray):
                _asin = item["asin"]
                try:
                    _title = item["title"]
                except Exception as e:
                    _title = default_book_title
                try:
                    _imUrl = item["imUrl"]
                except Exception as e:
                    _imUrl = default_img_Url
                filteredItem = {"asin":_asin, "title":_title, "imUrl":_imUrl}
                filteredArray.append(json.dumps(filteredItem))

        return filteredArray
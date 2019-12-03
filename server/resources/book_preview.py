from flask import render_template, make_response, request
from flask_restful import Resource, reqparse
from common.util import mongo
import json

default_book_title = "untitled"
default_img_Url = "no-url"
# mongodb_database = kindle_metadata

class BookPreviewResource(Resource):
    def regex_generator(self, arr):
        regex_string = "("
        for asin in arr:
            regex_string += str(asin) + "|"
    
        regex_string = regex_string[:-1] + ")"
        return regex_string

    def post(self):
        """Returns book information (lightweight)   
        Request Body: (asinArray) Array of string 
        Response Body: Array of json(asin,title,imUrl)"""
        parser = reqparse.RequestParser()
        parser.add_argument('page', type=int, location='args')
        parser.add_argument('count', type=int, location='args')
        args = parser.parse_args()
        json_request = request.get_json(force=True)
        _asinArray = json_request.get('asinArray')
        booksJSONArray = list()

        if (not args['count'] or not args['page']):
            bookInfo = mongo.db.kindle_metadata.find({"asin" : {"$regex": self.regex_generator(_asinArray) }}, {"asin" : 1, "title": 1, "imUrl": 1})
        else:
            _limit = args['count']
            _offset = (args['page']-1) * args['count']
            bookInfo = mongo.db.kindle_metadata.find({"asin" : {"$regex": self.regex_generator(_asinArray) }}, {"asin" : 1, "title": 1, "imUrl": 1}).skip(_offset).limit(_limit)

        for item in bookInfo:
            book_asin = item.get('asin')
            book_title = item.get('title')
            book_imUrl = item.get('imUrl')  
            bookLW = {"asin": book_asin, "title": book_title, "imUrl":book_imUrl}
            booksJSONArray.append(bookLW)

        return {"message": "Book previews shown", "asinArray": str(_asinArray), "body": booksJSONArray}, 200

class BookCategoryResource(Resource):
    def post(self):
        """Returns books that have categories containing categories in categoryArray
        Request Body: (categoryArray) Array of String 
        Response Body: Array of json(asin, title, imUrl)"""
        parser = reqparse.RequestParser()
        parser.add_argument('page', type=int, location='args')
        parser.add_argument('count', type=int, location='args')
        args = parser.parse_args()
        json_request = request.get_json(force=True)
        _categoryArray = json_request.get('categoryArray')
        filteredArray = list()

        if (not args['count'] or not args['page']):
            bookInfo = mongo.db.kindle_metadata.find({"categories.0": {"$elemMatch": {"$in": _categoryArray}}}, {"asin" : 1, "title": 1, "imUrl": 1})
        else:
            _limit = args['count']
            _offset = (args['page']-1) * args['count']
            bookInfo = mongo.db.kindle_metadata.find({"categories.0": {"$elemMatch": {"$in": _categoryArray}}}, {"asin" : 1, "title": 1, "imUrl": 1}).skip(_offset).limit(_limit)

        for item in bookInfo:
            book_asin = item.get('asin')
            book_title = item.get('title')
            book_imUrl = item.get('imUrl')  
            bookLW = {"asin": book_asin, "title": book_title, "imUrl":book_imUrl}
            filteredArray.append(bookLW)
        return {"message": "Books filtered based on categories", "categoryArray": str(_categoryArray), "body": filteredArray}, 200



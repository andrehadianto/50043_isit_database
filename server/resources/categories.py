from flask import render_template, make_response, request
from flask_restful import Resource, reqparse
from flask import json
from common.util import mongo
from bson.json_util import dumps, default


class CategoriesResource(Resource):
    """Returns all categories available"""
    def get(self):
        parser = reqparse.RequestParser()

        try:
            cursor = mongo.db.categories.find({})
            jsonstring = dumps(cursor, default=default)
            return json.loads(jsonstring), 200

        except Exception as e:
            print(e)
            return {"message": "Error calling all categories"}, 400
        

    """Check if category exists
            Parameters: array of input categories
            Return: array of new categories or None
            """
    def category_exists(self, categories):
        new_categories = []
        for cat in categories:
            cursor = mongo.db.categories.find_one({'categories': cat})
            
            if cursor == None:
                new_categories.append(cat)
            
        if len(new_categories) == 0:
            return None
        else:
            return new_categories

    """Add new category"""
    def post(self):
        req_json = request.get_json(force=True)

        try:
            _categoriesArr = req_json.get('categories')

        except Exception as e:
            print(e)
            return {"message": "category is a required field"}, 400

        add_categories = self.category_exists(_categoriesArr)
        print(add_categories)
        if add_categories != None:
            for cat in add_categories:
                letter = cat[0].upper()
                try:
                    mongo.db.categories.update_one({'letter': letter}, {'$push': {'categories': cat}})
                except Exception as e:
                    print(e)
                    return {"message": "error adding new category {}".format(cat)}, 400
            
            return {"message": "Successfully added new categories {}".format(add_categories)}, 200

        return {"message": "No new categories to add"}, 200
       

from flask import render_template, make_response, request
from flask_restful import Resource, reqparse
from flask import json
from common.util import mongo
from bson.json_util import dumps, default


class CategoriesResource(Resource):
    """Returns all categories available"""
    def get(self):
        parser = reqparse.RequestParser()
        cursor = mongo.db.categories.find({})
        jsonstring = dumps(cursor, default=default)
        return json.loads(jsonstring)
from flask import json
from flask_restful import Resource, request
from common.util import mongo
from bson.json_util import dumps, default

#get book by id or asin via query param
class getBookDetails(Resource):
    def get(self):
        fieldvalue = request.args.get('asin')
        cursor = mongo.db.kindle_metadata.find_one({'asin': fieldvalue})
        jsonstring = dumps(cursor, default=default)
        return json.loads(jsonstring)


from flask_restful import Resource, reqparse
from common.util import mongo_log
from datetime import datetime
from bson import ObjectId

MAX_STRING_LENGTH = 70
DEFAULT_COUNT = 50
DEFAULT_OFFSET = 0

class LogsList(Resource):
    """ Returns a list of loggings """
    def get(self):
        parser = reqparse.RequestParser()

        parser.add_argument('page', type=int, location='args')
        parser.add_argument('count', type=int, location='args')

        args = parser.parse_args()

        if not args['count'] or not args['page']:
            _limit = DEFAULT_COUNT
            _offset = DEFAULT_OFFSET
        else:
            _limit = args['count']
            _offset = (args['page'] - 1) * args['count']

        log_array = []
        logs = mongo_log.db.logs.find({}).limit(_limit).skip(_offset)
        for log in logs:
            time = log.get('time').strftime("%d-%m-%Y, %H:%M:%S")
            status = log.get('status')
            body = log.get('body')
            if len(body) > MAX_STRING_LENGTH:
                body = body[:MAX_STRING_LENGTH-1] + '...'
            json = {
                "time": time,
                "status": status,
                "body": body
            }
            log_array.append(json)
        return log_array

class LogAPI(Resource):
    """ Returns a specific log with respect to mongo ObjectId """
    def get(self, id):
        log = mongo_log.db.logs.find_one({'_id': ObjectId(id)})
        time = log.get('time').strftime("%d-%m-%Y, %H:%M:%S")
        status = log.get('status')
        body = log.get('body')
        json = {
            "time": time,
            "status": status,
            "body": body
        }
        return json

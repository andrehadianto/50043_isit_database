from flask_restful import Resource, reqparse
from common.util import con, cursor
import json
import time

def dictfetchall(cursor):
    """Returns all rows from a cursor as a list of dicts"""
    desc = cursor.description
    return [dict(zip([col[0] for col in desc], row)) 
            for row in cursor.fetchall()]

class ReviewListAPI(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('page', type=int, location='args')
        parser.add_argument('count', type=int, location='args')
        args = parser.parse_args()

        _limit = args['count']
        _offset = (args['page'] - 1) * args['count']

        cursor.execute("SELECT * FROM kindle_reviews LIMIT {} OFFSET {}".format(_limit, _offset))
        results = dictfetchall(cursor)

        # TO DO: error handling

        return results

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('asin', type=str, location='form')
        parser.add_argument('reviewText', type=str, location='form')
        parser.add_argument('reviewTime', type=str, location='form')
        parser.add_argument('reviewerID', type=str, location='form')
        parser.add_argument('reviewerName', type=str, location='form')
        parser.add_argument('summary', type=str, location='form')
        args = parser.parse_args()

        _asin = args['asin']
        _reviewText = args['reviewText']
        _reviewTime = args['reviewTime']
        _reviewerID = args['reviewerID']
        _reviewerName = args['reviewerName']
        _summary = args['summary']
        _unixReviewTime = int(time.time())

        # TO DO: fix auto increment id (mysql server issue?)

        sql = "INSERT INTO kindle_reviews (id, asin, reviewText, reviewTime, reviewerID, reviewerName, summary, unixReviewTime) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        val = (0, _asin, _reviewText, _reviewTime, _reviewerID, _reviewerName, _summary, _unixReviewTime)
        response = cursor.execute(sql, val)

        # TO DO: try/catch for insert (error handling)

        con.commit()

        return response

# class ReviewAPI(Resource):
#     def __init__(self):
#         self.reqparse = reqparse.RequestParser()
#         self.reqparse = reqparse.add_argument('id', type=int, location='json')
#         self.reqparse.add_argument('asin', type=str, location='json')
#         self.reqparse.add_argument('helpful', type=str, location='json')
#         self.reqparse.add_argument('overall', type=int, location='json')
#         self.reqparse.add_argument('reviewText', type=str, location='json')
#         self.reqparse.add_argument('reviewerID', type=str, location='json')
#         self.reqparse.add_argument('reviewerName', type=str, location='json')
#         self.reqparse.add_argument('summary', type=str, location='json')
#         self.reqparse.add_argument('unixReviewTime', type=int, location='json')
#         super(ReviewAPI, self).__init__()

#     def get(self, id):
#         pass

#     def put(self, id):
#         pass

#     def delete(self, id):
#         pass
from flask_restful import Resource, reqparse
from common.util import connect
import json
import time
import datetime

def dictfetchall(cursor):
    """Returns all rows from a cursor as a list of dicts"""
    desc = cursor.description
    return [dict(zip([col[0] for col in desc], row)) 
            for row in cursor.fetchall()]


class ReviewsAPI(Resource):
    def get(self, asin):
        parser = reqparse.RequestParser()

        parser.add_argument('page', type=int, location='args')
        parser.add_argument('count', type=int, location='args')

        args = parser.parse_args()

        if not args['count'] or not args['page']:
            _limit = 15
            _offset = 0
        else:
            _limit = args['count']
            _offset = (args['page'] - 1) * args['count']

        
        con, cursor = connect()
        try:
            cursor.execute("SELECT * FROM kindle_reviews where asin=%s LIMIT %s OFFSET %s", (asin, _limit, _offset))
            results = dictfetchall(cursor)
            return results
        except Exception as e:
            print(e)

        finally:
            con.close()

    def post(self, asin):
        parser = reqparse.RequestParser()
        parser.add_argument('overall', type=int, location='form', help="No rating")
        parser.add_argument('reviewText', type=str, location='form', help="No review text")
        parser.add_argument('reviewerID', type=str, location='form', help="Invalid user")
        parser.add_argument('reviewerName', type=str, location='form', help="Invalid user")
        parser.add_argument('summary', type=str, location='form', help="No summary")
        args = parser.parse_args()

        _helpful = "[0, 0]"
        _overall = args['overall']
        _reviewText = args['reviewText']
        _reviewerID = args['reviewerID']
        _reviewerName = args['reviewerName']
        _summary = args['summary']

        _unixReviewTime = int(time.time())
        _reviewTime = datetime.datetime.utcfromtimestamp(_unixReviewTime).strftime('%m %d, %Y')

        format_specifier_string = ('%s, '* 10).strip(', ')
        sql = "INSERT INTO kindle_reviews (id, asin, helpful, overall, reviewText, reviewTime, reviewerID, reviewerName, summary, unixReviewTime) VALUES (%s)" % format_specifier_string
        val = (None, asin, _helpful, _overall, _reviewText, _reviewTime, _reviewerID, _reviewerName, _summary, _unixReviewTime)
        
        con, cursor = connect()

        try:
            cursor.execute(sql, val)
            con.commit()
            return {"message": "Book review posted"}, 200
        
        except Exception as e:
            print(e)

        finally:
            con.close()

class ReviewAPI(Resource):
    def get(self, id):

        con, cursor = connect()

        try:
            cursor.execute("SELECT * FROM kindle_reviews where id=%s", (id,))
            results = dictfetchall(cursor)
            return results

        except Exception as e:
            print(e)

        finally:
            con.close()

    def delete(self, id):

        con, cursor = connect()

        try: 
            cursor.execute("DELETE FROM kindle_reviews where id=%s", (id,))
            con.commit()
            return {'message': 'Book review with id {} was deleted'.format(id)}, 200

        except Exception as e:
            print(e)
        
        finally:
            con.close()

    def put(self, id):

        parser = reqparse.RequestParser()
        parser.add_argument('reviewText', type=str, location='form', help="No review text")
        parser.add_argument('overall', type=int, location='form', help="No overall rating")
        parser.add_argument('summary', type=str, location='form', help="No summary")
        args = parser.parse_args()

        _reviewText = args['reviewText']
        _overall = args['overall']
        _summary = args['summary']

        _unixReviewTime = int(time.time())
        _reviewTime = datetime.datetime.utcfromtimestamp(_unixReviewTime).strftime('%m %d, %Y')

        sql = """UPDATE kindle_reviews 
                SET overall=%s, reviewText=%s, summary=%s, reviewTime=%s, unixReviewTime=%s 
                WHERE id=%s"""
        val = (_overall, _reviewText, _summary, _reviewTime, _unixReviewTime, id)

        con, cursor = connect()

        try:
            cursor.execute(sql, val)
            con.commit()
            response = {"message": "Book review with id {} was edited".format(id)}
            return response, 200

        except Exception as e:
            print(e)

        finally:
             con.close()

class ReviewsByUserAPI(Resource):
    def get(self, reviewerID):

        con, cursor = connect()

        try:
            cursor.execute("SELECT * FROM kindle_reviews where reviewerID='%s'", (reviewerID,))
            results = dictfetchall(cursor)
            return results

        except Exception as e:
            print(e)

        finally:
             con.close()

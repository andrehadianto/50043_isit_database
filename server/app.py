from flask import Flask, make_response, render_template, request
from flask_restful import Api
from resources.book_preview import BookPreviewResource, BookCategoryResource
from resources.categories import CategoriesResource
from resources.metadata import GetBookDetails, BooksListResource, RegisterNewBook, UpdateBookResource
from resources.test import testMySql, testMongo
from resources.review import ReviewsAPI, ReviewsByUserAPI, ReviewAPI
from resources.user import UserLogin, UserSignup
from resources.logs import LogsList, LogAPI
from common.util import mongo, mongo_log
import datetime
import logging

app = Flask(__name__,
    static_folder="../static/public",
    template_folder="../static"
    )

logging.basicConfig(level=logging.DEBUG,
					format="%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s")
@app.route('/isit/<path:path>')
@app.route('/isit', defaults={'path': '/isit'})
def index(path):
    return make_response(render_template("index.html"), 200, {'Content-type': 'text/html'})
api = Api(app)
api.add_resource(testMySql, '/mysql')
api.add_resource(testMongo, '/mongo')
api.add_resource(BookPreviewResource, '/books/previews')
api.add_resource(BookCategoryResource, '/books/category')
api.add_resource(CategoriesResource, '/categories')

api.add_resource(GetBookDetails, '/book/<string:asin>')
api.add_resource(BooksListResource, '/books')
api.add_resource(RegisterNewBook, '/book/new')
api.add_resource(UpdateBookResource, '/book/update/<string:asin>')

api.add_resource(ReviewsAPI, '/reviews/<asin>', endpoint = 'reviews')
api.add_resource(ReviewsByUserAPI, '/reviews/user/<reviewerID>', endpoint = 'reviews/user')
api.add_resource(ReviewAPI, '/review/<id>', endpoint = 'review')

api.add_resource(UserLogin, '/user/login')
api.add_resource(UserSignup, '/user/signup')

api.add_resource(LogsList, '/user/logs')
api.add_resource(LogAPI, '/user/logs/<string:id>', endpoint='user/logs')
# Invoked after every requests to log the timestamp, content & status
@app.after_request
def log_request(response):
    response.direct_passthrough = False
    time = datetime.datetime.now()
    body = response.data.decode("utf-8")
    status_as_string = response.status
    status_as_integer = response.status_code
    try:
        _id = mongo_log.db.logs.insert_one({
            "time": time,
            "body": body,
            "method": request.method,
            "path": request.full_path,
            "status": status_as_string,
            "status_code": status_as_integer
        })
        app.logger.debug("Successful log insert with _id %s" % _id)
    except:
        app.logger.warning("Error encountered during insertion of log to database")    
    return response
    
if __name__ == "__main__":
    app.run(host='0.0.0.0')

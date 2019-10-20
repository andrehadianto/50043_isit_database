from flask import Flask
from flask_restful import Api
from resources.foo import Foo, testMySql, testMongo
from resources.book_preview import BookPreviewResource, BookCategoryResource
from common.util import mongo, mongo_log
import datetime
import logging

app = Flask(__name__,
    static_folder="../static/public",
    template_folder="../static"
    )
logging.basicConfig(level=logging.DEBUG,
					format="%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s")
api = Api(app)
api.add_resource(Foo, '/')
api.add_resource(testMySql, '/mysql')
api.add_resource(testMongo, '/mongo')
#api.add_resource(MetaAPI, '/books')
api.add_resource(BookPreviewResource, '/books/previews')
api.add_resource(BookCategoryResource, '/books/category')

# Invoked after every requests to log the timestamp, content & status
@app.after_request
def log_request(response):
    response.direct_passthrough = False
    time = datetime.datetime.now()
    body = response.data.decode("utf-8")
    status_as_string = response.status
    status_as_integer = response.status_code
    try:
        _id = mongo_log.db.logs.insert({
            "time": time,
            "body": body,
            "status": status_as_string,
            "status_code": status_as_integer
        })
        app.logger.debug("Successful log insert with _id %s" % _id)
    except:
        app.logger.warning("Error encountered during insertion of log to database")    
    return response
    
if __name__ == "__main__":
    app.run(debug=True)
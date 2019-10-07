from flask import Flask
from flask_restful import Api
from resources.foo import Foo
import common.util
import datetime
import logging

app = Flask(__name__)
api = Api(app)
logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s")

@app.route('/hello', methods=['GET'])
def hello():
	return {'greeting': 'have a nice day'}

@app.route('/hello/<name>', methods=['GET'])
def greet(name):
	return {'greeting': "Hello {}. Have a nice day".format(name)}

@app.after_request
def log_request(response):
    time = datetime.datetime.now()
    body = response.data
    status_as_string = response.status
    status_as_integer = response.status_code
    try:
        _id = common.util.mongo.db.logs.insert({
            "time": time,
            "body": body,
            "status": status_as_string,
            "status_code": status_as_integer
        })
        app.logger.debug("Successful insert with _id %s" % _id)
    except:
        app.logger.warning("Error encountered during insertion of log")    
    return response
from flask import Flask
from flask_restful import Api
from resources.foo import Foo
import common.util

app = Flask(__name__)
api = Api(app)



    
from flask import render_template, make_response
from flask_restful import Resource
from common.util import mongo

class Foo(Resource):
    def get(self):
        headers = {'Content-type': 'text/html'}
        return make_response(render_template("index.html"),200,headers)
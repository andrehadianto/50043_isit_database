from flask import Flask
from flask_restful import Api
from resources.foo import Foo, testMySql, testMongo
import common.util

app = Flask(__name__,
    static_folder="../static/public",
    template_folder="../static"
    )

api = Api(app)
api.add_resource(Foo, '/')
api.add_resource(testMySql, '/mysql')
api.add_resource(testMongo, '/mongo')

if __name__ == "__main__":
    app.run(debug=True)
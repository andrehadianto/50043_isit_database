from flask import Flask
from flask_restful import Api
from resources.foo import Foo
import common.util

app = Flask(__name__,
    static_folder="../static/public",
    template_folder="../static"
    )

api = Api(app)
api.add_resource(Foo, '/')

if __name__ == "__main__":
    app.run(debug=True)
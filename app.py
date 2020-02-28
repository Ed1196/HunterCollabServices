"""
Necessary Modules
    Flask is a framework.
    Flask_Restful is an extension to Flask
"""
from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)



class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


# Adds the resource to our API
api.add_resource(HelloWorld, '/')

if __name__ == '__main__':
    from db import db
    app.run(debug=True)

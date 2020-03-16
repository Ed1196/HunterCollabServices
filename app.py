"""
Necessary Modules
    Flask is a framework.
    Flask_Restful(library) is an extension to Flask
    FLask_jwy_extended(plugin) enables login/logout functionality with JSON tokens
"""
from flask import Flask
from flask_restful import Resource, Api
from flask_jwt_extended import JWTManager
from resources.users import UserRegister, UserLogin, RefreshToken
from resources.collaborations import UserCollabs, AllCollabs

app = Flask(__name__)
api = Api(app)

app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "sqlite:///data.db"  # Config database URI that is used to connect to db.
app.config[
    "SQLALCHEMY_TRACK_MODIFICATIONS"
] = False  # Tracks modification of objects and emit signals. Not needed.
app.config["PROPAGATE_EXCEPTIONS"] = True  # Raises FLASK-JWT errors.
app.secret_key = "Edwin"

jwt = JWTManager(
    app
)  # Creates an object to hold JWT settings and callback funcs. No longer creates an /auth endpoint.


# Use to create local database.
@app.before_first_request
def create_tables():
    db.create_all()


class HelloWorld(Resource):
    def get(self):
        return {"hello": "world"}


# Adds the resource to our API
api.add_resource(HelloWorld, "/")
api.add_resource(UserRegister, "/register")
api.add_resource(UserLogin, "/login")
api.add_resource(AllCollabs, "/collabs")
api.add_resource(UserCollabs, "/user-collabs/<_id>")
api.add_resource(RefreshToken, "/refresh")

if __name__ == "__main__":
    from db import db

    db.init_app(app)  # Binds the instance of SQLAlchemy to this app.
    app.run(debug=True)

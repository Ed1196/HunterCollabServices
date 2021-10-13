"""
Necessary Modules
    Flask is a framework.
    Flask_Restful(library) is an extension to Flask
    FLask_jwy_extended(plugin) enables login/logout functionality with JSON tokens
"""
from flask import Flask
from flask_restful import Resource, Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from resources.users import User, UserSkills, UserClasses
from resources.currentUsers import CurrentUser, CurrentUserUpdate
from resources.auth import UserRegister, UserLogin, RefreshToken
from resources.collaborations import UserCollab, UserCollabs, AllCollabs, CreateCollab, InteractCollab
from resources.skills import Skills
from resources.classes import Classes

app = Flask(__name__)
api = Api(app)
CORS(app)

app.config[
    "SQLALCHEMY_DATABASE_URI"
] = 'postgres://hsjnrfhnzefrcr:6edcd64ecce0ce22b36a76839f557e8e21b170c7002429455e5f6aa31a8d2f35@ec2-34-205-14-168.compute-1.amazonaws.com:5432/d79mm76ttheq46'
# "sqlite:///data.db"  # Config database URI that is used to connect to db.
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
api.add_resource(UserLogin, "/auth/login")
api.add_resource(RefreshToken, "/refresh")

api.add_resource(User, "/user/<_email>")
api.add_resource(CurrentUser, "/user")
api.add_resource(UserSkills, "/user/skills/<_email>")
api.add_resource(UserClasses, "/user/classes/<_email>")
api.add_resource(CurrentUserUpdate, "/user-update/<_field>")

api.add_resource(Skills, "/skills/<_chars>")
api.add_resource(Classes, "/classes/<_chars>")

api.add_resource(CreateCollab, "/user-collab")
api.add_resource(UserCollab, "/user-collab/<_id>")
api.add_resource(UserCollabs, "/user-collabs/<_type>")
api.add_resource(InteractCollab, "/interact-collab")

api.add_resource(AllCollabs, "/collabs")


if __name__ == "__main__":
    from db import db

    db.init_app(app)  # Binds the instance of SQLAlchemy to this app.
    app.run(debug=True)

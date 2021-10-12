from flask import request
from flask_restful import Resource, reqparse
from models.users import UserModel
from models.skills import SkillsModel
from schemas.users import UserSchema
from werkzeug.security import safe_str_cmp
from marshmallow import ValidationError
import json
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    fresh_jwt_required,
    jwt_refresh_token_required,
    get_jwt_identity
)

BLANK_ERROR = "{} cannot be left blank!"
CREDENTIAL_ERROR = "Invalid Credentials."
RETRIEVAL_ERROR = "Error retrieving user."

user_schema = UserSchema()


class User(Resource):
    """
            A class used to represent an external representation(endpoint) of a User entity that deals
            with user details. The User Resource will allow developers access to the API via
            calls get, put, delete and post. They will be able to retrieve and edit User details.

            Args
            ----
            Resource: Flask RESTful class that will wrap the UserRegister class. Gives class access to HTTP methods.


            Methods
            -------
            Method that handles the response that will be created when a user sends a request to the API.
            get(): Handles post request to the endpoint associated with User. Will retrieve a users details.
    """
    @jwt_required
    def get(self, _email):
        try:
            user = UserModel.find_by_email(_email)
            if user is not None:
                return {"success": True, "user": user.json()}, 200
            return {"success": False, "message": RETRIEVAL_ERROR}
        except ValidationError as err:
            return err.messages, 400


class UserSkills(Resource):
    @jwt_required
    def get(self, _email):
        try:
            user = UserModel.find_by_email(_email)
            if user is not None:
                skills = [skill.name for skill in user.skillsList]
                return {"success": True, "skills": skills }, 200
        except ValidationError as err:
            return err.messages, 400
        return {"success": False, "message": RETRIEVAL_ERROR}


class UserClasses(Resource):
    @jwt_required
    def get(self, _email):
        try:
            user = UserModel.find_by_email(_email)
            if user is not None:
                classes = [_class.name for _class in user.classesList]
                return {"success": True, "classes": classes }, 200
        except ValidationError as err:
            return err.messages, 400
        return {"success": False, "message": RETRIEVAL_ERROR}


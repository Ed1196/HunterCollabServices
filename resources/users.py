from flask import request
from flask_restful import Resource, reqparse
from models.users import UserModel
from schemas.users import UserSchema
from werkzeug.security import safe_str_cmp
from marshmallow import ValidationError
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

user_schema = UserSchema()


class UserRegister(Resource):
    """
        A class used to represent an external representation of a User entity that deals with register.
        The UserRegister Resource will allow developers access to the API via calls get, put, delete and post.

        Args
        ----
        Resource: Flask RESTful class that will wrap the UserRegister class. Gives class access to HTTP methods.


        Attributes
        ----------
        _user_parser: Variable that will allow us to specify and retrieve data from the payload from the endpoint call.

        Methods
        -------
        post(): Method that handles the response that will be created when a user sends a request to the API.
                Handles post request to the endpoint associated with UserRegister. Will register a user.

        """

    def post(self):
        try:
            data = user_schema.load(request.get_json())
        except ValidationError as err:
            return err.messages, 400

        if UserModel.find_by_email(data["email"]):
            return {"message": "Email already used!"}

        user = UserModel(**data)
        user.save_to_db()

        return {"message": "User created succesfully!"}, 201


class UserLogin(Resource):


    @classmethod
    def post(cls):
        try:
            data = user_schema.load(request.get_json())
        except ValidationError as err:
            return err.messages, 400
        user = UserModel.find_by_email(data["email"])
        if user and safe_str_cmp(user.password, data["password"]):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {"access_token": access_token, "refresh_token": refresh_token}, 200
        return {"message": CREDENTIAL_ERROR}, 401


class RefreshToken(Resource):
    @classmethod
    @jwt_refresh_token_required
    def get(cls):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {'access_token': new_token}, 200




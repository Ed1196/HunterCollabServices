from flask_restful import Resource, reqparse
from flask import request
from flask_jwt_extended import jwt_required, fresh_jwt_required, get_jwt_identity
from models.collaborations import CollabModel


class Collaboration(Resource):
    """
            A class used to represent an external representation(endpoint) of a Collaboration entity that deals
            with user collaborations. The Collaboration Resource will allow developers access to the API via
            calls get, put, delete and post. They will be able to create, retrieve, delete and update collaborations.

            Args
            ----
            Resource: Flask RESTful class that will wrap the UserRegister class. Gives class access to HTTP methods.


            Attributes
            ----------
            _collab_parser: Variable that will allow the user to specify and retrieve data from the payload.

            Methods
            -------
            Method that handles the response that will be created when a user sends a request to the API.
            post(): Handles post request to the endpoint associated with Collaboration. Will create a collaboration.
            get(): Handles get request to the endpoint associated with Collaboration. Will retrieve all collaboration.
    """

    _collab_parser = reqparse.RequestParser()

    @jwt_required
    def post(self):
        data = request.get_json()

        collab = CollabModel(**data)
        try:
            collab.save_to_db()
            CollabModel.add_skills_to_list(collab)
            CollabModel.add_classes_to_list(collab)
            CollabModel.add_member_to_list(collab)
        except:
            return {'success': False, 'message': 'An error occured while creating the collaboration!.'}, 500

        return {'success': True, 'collab': collab.json()}

    @jwt_required
    def get(self):
        user_id = get_jwt_identity()
        collabs = [collab.json() for collab in CollabModel.find_all()]
        if user_id is not None:
            return {'success': True, 'collabs': collabs}, 200
        return {'success': False, 'message': 'Invalid Auth, please log in.'}

from flask_restful import Resource, reqparse
from flask import request
from flask_jwt_extended import jwt_required, fresh_jwt_required
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
    """

    _collab_parser = reqparse.RequestParser()

    def post(self):
        data = request.get_json()

        collab = CollabModel(**data)
        collab.save_to_db()
        CollabModel.add_skills_to_list(collab)
        CollabModel.add_classes_to_list(collab)
        CollabModel.add_member_to_list(collab)
        try:
            pass
        except:
            return {'success': False, 'message': 'An error occured while creating the collaboration!.'}, 500

        return {'success': True, 'collab': collab.json()}

from flask_restful import Resource, reqparse
from flask import request
from flask_jwt_extended import jwt_required, fresh_jwt_required, get_jwt_identity
from models.collaborations import CollabModel


class UserCollabs(Resource):
    """
        A class used to represent an external representation(endpoint) of a Collaboration entity that deals
        with user collaborations. The Collaboration Resource will allow developers access to the API via
        calls get, put, delete and post. They will be able to create, retrieve, delete and update collaborations.

        Args
        ----
        Resource: Flask RESTful class that will wrap the UserRegister class. Gives class access to HTTP methods.


        Attributes
        ----------
        _collab_parser: Variable that will allow the user to specify and retrieve data from the payload when the
                        a request is made to the api.

        Methods
        -------
        Method that handles the response that will be created when a user sends a request to the API.
        post(): Handles post request to the endpoint associated with Collaboration. Will create a collaboration.
        get(): Handles get request to the endpoint associated with Collaboration. Will retrieve all collaboration.
    """

    _collab_parser = reqparse.RequestParser()

    @jwt_required
    def post(self, _id):
        """Handles post request to the endpoint associated with UserCollabs. Will create a collaboration.

        This method will create a new collaboration in the collaborations table. It will also set up the
        association tables that will link the skills table, classes table and users table to the collaborations table.
        Each collaboration will be linked, in a many-to-many patter, to specified skills, classes and members that are
        part of the collaboration

        :param _id: Will not be used when posting a new collab.
        :return: JSON with a success message. Also a collab in json format if success is true.
                 The JSON will contains collab details.
        """
        data = request.get_json()

        collab = CollabModel(**data)
        try:
            collab.save_to_db()  # creates collab in table
            CollabModel.add_skills_to_list(collab)  # sets up association to skills table
            CollabModel.add_classes_to_list(collab)  # sets up association to classes table
            CollabModel.add_member_to_list(collab)  # sets up association to users table
        except:
            return {'success': False, 'message': 'An error occured while creating the collaboration!.'}, 500

        return {'success': True, 'collab': collab.json()}

    @jwt_required
    def get(self, _id):
        """Handles get request to the endpoint associated with UserCollabs.
           Will retrieve a single collab or all collabs for a user.

        :param _id: Id of the collab that needs to be retrieved.
        :return: The specified collab or all of a users collab.
        """
        user_id = get_jwt_identity()
        if _id != "None":
            collabs = (CollabModel.find_by_id(int(_id))).json()
        else:
            collabs = [collab.json() for collab in CollabModel.find_user_collabs(user_id)]

        if collabs is not None:
            return {'success': True, 'collabs': collabs}, 200
        return {'success': False, 'message': 'Error retrieving collaborations.'}

    @jwt_required
    def put(self, _id):
        data = request.get_json()
        collab = CollabModel.find_by_id(_id)
        if collab is not None:
            collab.update_data(data)
            collab.save_to_db()
            return {'success': True, 'collab': collab.json()}, 200
        return {'success': False, 'message': 'Error retrieving collaboration.'}

    @jwt_required
    def delete(self, _id):
        collab = CollabModel.find_by_id(_id)
        if collab is not None:
            # item calls its delete function to delete itself
            collab.delete_from_db()
            return {'succes': True, 'message': 'Collab succesfully deleted!'}, 200

        return {'succes': False, 'message': 'Item was not found!'}


class AllCollabs(Resource):

    @jwt_required
    def get(self):
        """Handles get request to the endpoint associated with Collaboration. Will retrieve all collaboration.

        This method retrieves the users identity from the JWT token.
        """
        collabs = [collab.json() for collab in CollabModel.find_all()]
        if collabs is not None:
            return {'success': True, 'collabs': collabs}, 200
        return {'success': False, 'message': 'Error retrieving collaborations.'}

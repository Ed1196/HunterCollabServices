from flask_restful import Resource, reqparse
from flask import request
from flask_jwt_extended import jwt_required, fresh_jwt_required, get_jwt_identity
from models.collaborations import CollabModel
from marshmallow import ValidationError
from schemas.collaborations import CollabSchema
from models.skills import SkillsModel
from models.classes import ClassesModel
from models.users import UserModel
import datetime
RETRIEVAL_ERROR = "Error retrieving collaborations."
DELETE_SUCCESSFUL = "Collab successfully deleted!"


# collab_schema = CollabSchema()

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

    @jwt_required
    def get(self, _type):
        """Handles get request to the endpoint associated with UserCollabs.
           Will retrieve a single collab or all collabs for a user.

        :param _id: Id of the collab that needs to be retrieved.
        :return: The specified collab or all of a users collab.
        """
        user_id = get_jwt_identity()
        user = UserModel.find_by_id(user_id)
        collabs = []
        if _type == "my-collabs":
            collabs = [
                collab.json() for collab in user.collabsList
            ]
        elif _type == "all-collabs":
            allCollabs = CollabModel.find_all()
            collabs = [
                collab.json() for collab in allCollabs
            ]
        elif _type == "rec-collabs":
            recCollabs = CollabModel.find_rec_collabs(user)
            collabs = [
                collab.json() for collab in recCollabs
            ]

        if collabs is not None:
            return {"success": True, "collabs": collabs}, 200
        return {"success": False, "message": RETRIEVAL_ERROR}


class CreateCollab(Resource):
    @jwt_required
    def post(self):
        """Handles post request to the endpoint associated with UserCollabs. Will create a collaboration.

        This method will create a new collaboration in the collaborations table. It will also set up the
        association tables that will link the skills table, classes table and users table to the collaborations table.
        Each collaboration will be linked, in a many-to-many patter, to specified skills, classes and members that are
        part of the collaboration

        :param _id: Will not be used when posting a new collab.
        :return: JSON with a success message. Also a collab in json format if success is true.
                 The JSON will contains collab details.
        """
        collabSkills = []
        collabClasses = []
        user_id = get_jwt_identity()
        user = UserModel.find_by_id(user_id)
        try:
            jsonData = request.get_json()
            jsonData['owner'] = user.email
            jsonData['status'] = True
            for skill in jsonData["skills"]:
                collabSkills.append(skill)
                if SkillsModel.find_by_name(skill) is None:
                    newSkill = SkillsModel(skill)
                    newSkill.save_to_db()

            for class_ in jsonData["classes"]:
                collabClasses.append(class_)
                if ClassesModel.find_by_name(class_) is None:
                    newClass = ClassesModel(class_)
                    newClass.save_to_db()

            del jsonData['skills']
            del jsonData['classes']
            # data = collab_schema.load(jsonData)
        except ValidationError as err:
            return err.messages, 400

        collab = CollabModel(**jsonData)

        try:

            collab.save_to_db()  # creates collab in table
            CollabModel.add_skills_to_list(collab, collabSkills)  # sets up association to skills table
            CollabModel.add_classes_to_list(collab, collabClasses)  # sets up association to classes table
            CollabModel.add_member_to_list(collab, user)  # sets up association to users table
            user.add_collab_to_user(collab)

        except ValidationError as err:
            return (
                {
                    "success": False,
                    "message": "An error occured while creating the collaboration!.",
                },
                500,
            )

        return {"success": True, "collab": collab.json()}


class UserCollab(Resource):
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

    @jwt_required
    def get(self, _id):
        """Handles get request to the endpoint associated with UserCollabs.
           Will retrieve a single collab or all collabs for a user.

        :param _id: Id of the collab that needs to be retrieved.
        :return: The specified collab or all of a users collab.
        """
        if _id != "None":
            collabs = CollabModel.find_by_id(_id)
        else:
            return {"success": False, "message": RETRIEVAL_ERROR}

        if collabs is not None:
            return {"success": True, "collab": collabs.json()}, 200
        return {"success": False, "message": RETRIEVAL_ERROR}

    @jwt_required
    def put(self, _id):
        data = request.get_json()
        collab = CollabModel.find_by_id(_id)
        if collab is not None:
            collab.update_data(data)
            collab.save_to_db()
            return {"success": True, "collab": collab.json()}, 200
        return {"success": False, "message": RETRIEVAL_ERROR}

    @jwt_required
    def delete(self, _id):
        collab = CollabModel.find_by_id(_id)
        if collab is not None:
            # item calls its delete function to delete itself
            collab.delete_from_db()
            return {"success": True, "message": DELETE_SUCCESSFUL}, 200

        return {"success": False, "message": RETRIEVAL_ERROR}


class AllCollabs(Resource):
    @jwt_required
    def get(self):
        """Handles get request to the endpoint associated with Collaboration. Will retrieve all collaboration.

        This method retrieves the users identity from the JWT token.
        """
        collabs = [collab.json() for collab in CollabModel.find_all()]
        if collabs is not None:
            return {"success": True, "collabs": collabs}, 200
        return {"success": False, "message": RETRIEVAL_ERROR}


class InteractCollab(Resource):
    @jwt_required
    def post(self):
        data = request.get_json()
        user_id = get_jwt_identity()
        user = UserModel.find_by_id(user_id)
        collab = CollabModel.find_by_id(data["id"])
        if collab is not None:
            if data["action"] == "join":
                if len(collab.membersList) + 1 == collab.size:
                    return {"success": False, "message": "Collab is full."}
                collab.add_member_to_list(collab, user)
                user.add_collab_to_user(collab)
            elif data["action"] == "leave":
                collab.remove_member_to_list(collab, user)
                user.remove_collab_from_user(collab)
            return {"success": True}, 200
        return {"success": False, "message": RETRIEVAL_ERROR}
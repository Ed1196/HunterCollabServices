from flask import request
from flask_restful import Resource, reqparse
from models.users import UserModel
from models.skills import SkillsModel
from models.classes import ClassesModel
from schemas.users import UserSchema
from werkzeug.security import safe_str_cmp
from marshmallow import ValidationError
import json
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity
)

BLANK_ERROR = "{} cannot be left blank!"
CREDENTIAL_ERROR = "Invalid Credentials."
RETRIEVAL_ERROR = "Error retrieving user."

user_schema = UserSchema()


class CurrentUser(Resource):
    @jwt_required()
    def get(self):
        try:
            user_id = get_jwt_identity()
            user = UserModel.find_by_id(user_id)
            if user is not None:
                return {"success": True, "user": user.json()}, 200
        except ValidationError as err:
            return err.messages, 400
        return {"success": False, "message": RETRIEVAL_ERROR}


class CurrentUserUpdate(Resource):
    @jwt_required()
    def post(self, _field):
        try:
            user_id = get_jwt_identity()
            user = UserModel.find_by_id(user_id)
            if user is not None:
                if _field == "skills":
                    jsonData = request.get_json()
                    user.empty_skill_list()
                    newSkills = []
                    for skill in jsonData["skills"]:
                        newSkills.append(skill)
                        if SkillsModel.find_by_name(skill) is None:
                            newSkill = SkillsModel(skill)
                            newSkill.save_to_db()
                    UserModel.add_skills_to_user(user, newSkills)
                    return {"success": True, "messages": "Successfully updated skills."}, 200
                if _field == "classes":
                    jsonData = request.get_json()
                    user.empty_class_list()
                    newClasses = []
                    for _class in jsonData["classes"]:
                        newClasses.append(_class)
                        if ClassesModel.find_by_name(_class) is None:
                            newClass = ClassesModel(_class)
                            newClass.save_to_db()
                    UserModel.add_classes_to_user(user, newClasses)
                    return {"success": True, "messages": "Successfully updated classes."}, 200
                if _field == "details":
                    jsonData = request.get_json()
                    user.github = jsonData["github"]
                    user.linkedIn = jsonData["linkedIn"]
                    user.username = jsonData["username"]
                    user.save_to_db()
                    return {"success": True, "messages": "Successfully updated details."}, 200

        except ValidationError as err:
            return err.messages, 400
        return {"success": False, "message": RETRIEVAL_ERROR}

from flask_restful import Resource
from flask_jwt_extended import jwt_required
from models.skills import SkillsModel

RETRIEVAL_ERROR = "Error retrieving skills."


class Skills(Resource):

    @jwt_required()
    def get(self, _chars):
        skills = [skill.name for skill in SkillsModel.starts_with(_chars)]
        if skills is not None:
            return {"success": True, "skills": skills}, 200
        return {"success": False, "message": RETRIEVAL_ERROR}



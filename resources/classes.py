from flask_restful import Resource
from flask_jwt_extended import jwt_required
from models.classes import ClassesModel

RETRIEVAL_ERROR = "Error retrieving skills."


class Classes(Resource):

    @jwt_required()
    def get(self, _chars):
        classes = [_class.name for _class in ClassesModel.starts_with(_chars)]
        if classes is not None:
            return {"success": True, "classes": classes}, 200
        return {"success": False, "message": RETRIEVAL_ERROR}



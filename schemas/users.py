from marshmallow import Schema, fields
from .collaborations import SkillSchema, ClassSchema, CollabSchema


class UserSchema(Schema):
    class Meta:
        load_only = ("password",)
        dump_only = ("id",)

    id = fields.Int()
    email = fields.Str(required=True)
    password = fields.Str(required=True)
    skills = fields.Nested(SkillSchema, many=True)
    classes = fields.Nested(ClassSchema, many=True)
    collabs = fields.Nested(CollabSchema, many=True, required=False)

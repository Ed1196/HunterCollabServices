from marshmallow import Schema, fields

from models.classes import ClassesModel
from models.skills import SkillsModel
from models.users import UserModel


class CollabSchema(Schema):
    class Meta:
        load_only = ("password",)
        dump_only = ("id",)

    id = fields.Int()
    owner = fields.Str()
    size = fields.Int()
    date = fields.Int()
    duration = fields.Int()
    location = fields.Str()
    status = fields.Bool()
    title = fields.Str()
    description = fields.Str()
    # Third attribute, in the table we want to connect this table to, that will update the association table

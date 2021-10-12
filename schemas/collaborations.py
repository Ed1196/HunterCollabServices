from marshmallow import Schema, fields


class SkillSchema(Schema):
    class Meta:
        dump_only = ("id",)

    id = fields.Int()
    name = fields.Str()


class ClassSchema(Schema):
    class Meta:
        dump_only = ("id",)

    id = fields.Int()
    name = fields.Str()


class CollabSchema(Schema):
    class Meta:
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
    skills = fields.Nested(SkillSchema, many=True)
    classes = fields.Nested(ClassSchema, many=True)
    # Third attribute, in the table we want to connect this table to, that will update the association table

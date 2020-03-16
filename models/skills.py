from typing import Dict, List, Union
from db import db


# Custom(custom JSON) return type, will help with type hinting.
SkillsJSON = Dict[str, Union[int, str]]


class SkillsModel(db.Model):
    """
        A child class used to represent skills model. Will have a one to many relationship with UsersModel class.

        Arga
        ----
        db.Model: Model extends db. Lets sqlAlchemy that SkillsModel will be stored in the database

        Attributes
        ----------
        __tablename__: Name of the table in the database.
        name: Name of a skill that a user has. Example Angular, Python, SQl , etc.

        Methods
        -------

    """

    __tablename__ = "skills"
    id = db.Column(db.Integer, primary_key="True")
    name = db.Column(db.String(40), unique=True)

    def __init__(self, skillName: str):
        self.name = skillName

    def json(self):
        return {"id": self.id, "name": self.name}

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_name(cls, name: str) -> "SkillsModel":
        return cls.query.filter_by(name=name).first()

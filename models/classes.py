from typing import Dict, List, Union
from db import db

# Custom(custom JSON) return type, will help with type hinting.
ClassesJSON = Dict[str, Union[int, str]]


class ClassesModel(db.Model):
    __tablename__ = "classes"
    id = db.Column(db.Integer, primary_key="True")
    name = db.Column(db.String(40), unique=True)

    def __init__(self, className: str):
        self.name = className

    def json(self) -> ClassesJSON:
        return {"id": self.id, "name": self.name}

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_name(cls, name) -> "ClassesModel":
        return cls.query.filter_by(name=name).first()

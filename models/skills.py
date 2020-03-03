from db import db


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
    __tablename__ = 'skills'
    id = db.Column(db.Integer, primary_key="True")
    name = db.Column(db.String(40))

    def __init__(self, skillName):
        self.name = skillName

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()



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
        skills_name: Name of a skill that a user has. Example Angular, Python, SQl , etc.
        user_id: Associates the SkillsModel class to the UsersModel class via the backref declared in the
                    UsersModel class. We can access the users that have this skill in their array.

        Methods
        -------

    """
    __tablename__ = 'skills'
    id = db.Column(db.Integer, primary_key="True")
    skills_name = db.Column(db.String(40))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)



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
        user_id: Associates the SkillsModel class to the UsersModel class via the backref declared in the
                 UsersModel class.

        Methods
        -------

    """
    __tablename__ = 'skills'
    skills_name = db.Column(db.String(40))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


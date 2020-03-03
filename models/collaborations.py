from db import db
from models.users import UserModel
from models.skills import SkillsModel
from models.classes import ClassesModel

"""
Association table that will be the connector in a Many-to-Many relationship between two tables(collaborations,skills).
Will associate skills requied for a collab to the collabs that have specified them. 
"""
skills = db.Table('collab_skills',
                  db.Column('collab_id', db.Integer, db.ForeignKey('collaborations.id')),
                  db.Column('skill_id', db.Integer, db.ForeignKey('skills.id')))


class CollabModel(db.Model):
    """
    A class used to represent an internal representation of a Collab entity. The CollabModel will be a helper file
    that will aid the programmer in development of the API.

    Args
    ----
    db.Model: Model extends db. Lets sqlAlchemy that UserModel will be stored in the database

    Attributes
    ----------
    id: Generates the id for the collab in the collaborations table
    owner: Email of the user that created the collab
    size: Size of the collab
    date: Date of when the collab was created
    duration: When will the collab end.
    location: Location of the collab
    status: Will determine if a collab is active or not
    title: Title of a collab
    description: Collaboration description
    skillsList: Will help update the association table

    Methods
    -------
    __init__(self, owner, size, date, duration, location, status, title, description, classes, skills, members)
        Initializes an object of class CollabModel. This object will have access to all of its methods and fields.
    json()
        Will turn all of CollabModel attributes and convert them to json format.
    add_to_skills_to_list(collab)
        __init__() will not create skills in the db. Initially skills is just an list of skills. This method parses
        that list and creates a skill in the db with that name. It creates it and also maps it to the collab that
        requires it.
    save_to_db()
        Uses the current session to create a new collab in the collaborations table in the db.
    """
    __tablename__ = 'collaborations'
    id = db.Column(db.Integer, primary_key=True)
    owner = db.Column(db.String(30))
    size = db.Column(db.Integer)
    date = db.Column(db.Integer)
    duration = db.Column(db.Integer)
    location = db.Column(db.String(30))
    status = db.Column(db.Boolean, default=False, server_default="false")
    title = db.Column(db.String(30))
    description = db.Column(db.String(256))
    # Third attribute that will update the association table
    skillsList = db.relationship('SkillsModel', secondary=skills, backref=db.backref('collabs', lazy='dynamic'))

    def __init__(self,
                 owner,
                 size,
                 date,
                 duration,
                 location,
                 status,
                 title,
                 description,
                 classes,
                 skills,
                 members):
        self.owner = owner
        self.size = size
        self.date = date
        self.duration = duration
        self.location = location
        self.status = status
        self.title = title
        self.description = description
        self.skills = skills

    def json(self):
        return {
            "owner": self.owner,
            "size": self.size,
            "date": self.date,
            "duration": self.duration,
            "location": self.location,
            "status": self.status,
            "title": self.title,
            "description": self.description,
            "skills": [skill.name for skill in self.skillsList]
        }

    @classmethod
    def add_to_skills_to_list(cls, collab):
        for skillName in collab.skills:
            skill = SkillsModel(skillName)
            skill.save_to_db()
            skill.collabs.append(collab)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

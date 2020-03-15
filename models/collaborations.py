from db import db
from models.users import UserModel
from models.skills import SkillsModel
from models.classes import ClassesModel

"""
Association tables that will be the connector in a Many-to-Many relationship between two tables.
    skills: Will associate skills required for a collab to the collabs that have specified them.
    classes: Will associate classes required for a collab to the collabs that have specified them.
    members: Will associate members required for a collab to the collabs that the user has joined 
"""
skills_association = db.Table('collab_skills',
                              db.Column('collab_id', db.Integer, db.ForeignKey('collaborations.id')),
                              db.Column('skill_id', db.Integer, db.ForeignKey('skills.id')))

classes_association = db.Table('collab_classes',
                               db.Column('collab_id', db.Integer, db.ForeignKey('collaborations.id')),
                               db.Column('class_id', db.Integer, db.ForeignKey('classes.id')))

members_association = db.Table('collab_members',
                               db.Column('collab_id', db.Integer, db.ForeignKey('collaborations.id')),
                               db.Column('member_id', db.Integer, db.ForeignKey('users.id')))


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
    skillsList: Will help update the association table between collab and skills or classes.

    Methods
    -------
    __init__(self, owner, size, date, duration, location, status, title, description, classes, skills, members)
        Initializes an object of class CollabModel. This object will have access to all of its methods and fields.
    json()
        Will turn all of CollabModel attributes and convert them to json format.
    save_to_db()
        Uses the current session to create a new collab in the collaborations table in the db.
    add_to_skills_to_list(collab)
        __init__() will not create skills in the db. Initially skills is just an list of skills. This method parses
        that list and creates a skill in the db with that name. It creates it and also maps it to the collab that
        requires it.
    def add_classes_to_list(collab)
        __init__() will not create skills in the db. Initially classes is just an list of classes. This method parses
        that list and creates a course in the db with that name. It creates it and also maps it to the collab that
        requires it.
    def add_member_to_list(cls, collab)
        This method parses the list of members and associates them to the collab they are part of in
        the associative table.
    def find_all()
        Queries for all the collabs

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
    # Third attribute, in the table we want to connect this table to, that will update the association table
    skillsList = db.relationship('SkillsModel',
                                 secondary=skills_association,
                                 backref=db.backref('collabs', lazy='joined'))
    classesList = db.relationship('ClassesModel',
                                  secondary=classes_association,
                                  backref=db.backref('collabs', lazy='joined'))
    membersList = db.relationship('UserModel',
                                  secondary=members_association,
                                  backref=db.backref('collabs'), lazy='joined')

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
        self.classes = classes
        self.members = members

    def json(self):
        return {
            "id": self.id,
            "owner": self.owner,
            "size": self.size,
            "date": self.date,
            "duration": self.duration,
            "location": self.location,
            "status": self.status,
            "title": self.title,
            "description": self.description,
            "skills": [skill.name for skill in self.skillsList],
            "classes": [course.name for course in self.classesList],
            "members": [member.email for member in self.membersList],
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def update_data(self, data):
        self.size = data['size']
        self.date = data['date']
        self.duration = data['duration']
        self.location = data['location']
        self.status = data['status']
        self.title = data['title']
        self.description = data['description']
        self.skills = data['skills']
        self.classes = data['classes']

    @classmethod
    def add_skills_to_list(cls, collab):
        for skillName in collab.skills:
            skill = SkillsModel(skillName)
            skill.save_to_db()
            skill.collabs.append(collab)
            db.session.commit()

    @classmethod
    def add_classes_to_list(cls, collab):
        for className in collab.classes:
            course = ClassesModel(className)
            course.save_to_db()
            course.collabs.append(collab)
            db.session.commit()

    @classmethod
    def add_member_to_list(cls, collab):
        for memberName in collab.members:
            user = UserModel.find_by_email(memberName)
            user.collabs.append(collab)
            db.session.commit()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def find_user_collabs(cls, user_id):
        user = UserModel.find_by_id(user_id)
        return cls.query.filter_by(owner=user.email).all()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
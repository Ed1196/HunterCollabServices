from typing import Dict, List, Union
from db import db
from models.skills import SkillsModel, SkillsJSON
from models.classes import ClassesModel, ClassesJSON
import math

# Custom(custom JSON) return type, will help with type hinting
CollabJSON = Dict[
    str, Union[int, str, int, int, int, str, bool, str, str, List, List, List]
]

"""
Association tables that will be the connector in a Many-to-Many relationship between two tables.
    skills: Will associate skills required for a collab to the collabs that have specified them.
    classes: Will associate classes required for a collab to the collabs that have specified them.
    members: Will associate members required for a collab to the collabs that the user has joined 
"""
skills_association = db.Table(
    "collab_skills",
    db.Column("collab_id", db.Integer, db.ForeignKey("collaborations.id")),
    db.Column("skill_id", db.Integer, db.ForeignKey("skills.id")),
)

classes_association = db.Table(
    "collab_classes",
    db.Column("collab_id", db.Integer, db.ForeignKey("collaborations.id")),
    db.Column("class_id", db.Integer, db.ForeignKey("classes.id")),
)

members_association = db.Table(
    "collab_members",
    db.Column("collab_id", db.Integer, db.ForeignKey("collaborations.id")),
    db.Column("member_id", db.Integer, db.ForeignKey("users.id")),
)


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

    __tablename__ = "collaborations"
    id = db.Column(db.Integer, primary_key=True)
    owner = db.Column(db.String(320))
    size = db.Column(db.Integer)
    date = db.Column(db.String(100))
    duration = db.Column(db.String(100))
    location = db.Column(db.String(100))
    status = db.Column(db.Boolean, default=False, server_default="false")
    title = db.Column(db.String(100))
    description = db.Column(db.String(256))
    # Third attribute, in the table we want to connect this table to, that will update the association table
    skillsList = db.relationship(
        "SkillsModel",
        secondary=skills_association,
        backref=db.backref("collabs", lazy="joined"),
    )
    classesList = db.relationship(
        "ClassesModel",
        secondary=classes_association,
        backref=db.backref("collabs", lazy="joined"),
    )
    membersList = db.relationship(
        "UserModel",
        secondary=members_association,
        backref=db.backref("collabs"),
        lazy="joined",
    )

    def __eq__(self, other):
        return self.id == other.id

    def __init__(
        self,
        owner: str,
        size: int,
        date: str,
        duration:str,
        location: str,
        status: bool,
        title: str,
        description: str,
        classes: List = [],
        skills: List = [],
        members: List = [],
    ):
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

    def json(self) -> CollabJSON:
        return {
            "id": self.id,
            "owner": self.owner,
            "size": self.size,
            "date": int(self.date),
            "duration": int(self.duration),
            "location": self.location,
            "status": self.status,
            "title": self.title,
            "description": self.description,
            "skills": [skill.name for skill in self.skillsList],
            "classes": [course.name for course in self.classesList],
            "members": [member.email for member in self.membersList],
        }

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()

    def update_data(self, data) -> None:
        self.size = data["size"]
        self.date = data["date"]
        self.duration = data["duration"]
        self.location = data["location"]
        # self.status = data["status"]
        self.title = data["title"]
        self.description = data["description"]
        self.add_skills_to_list(self, data["skills"])
        self.add_classes_to_list(self, data["classes"])

    def empty_class_list(self):
        self.classesList.clear()
        db.session.commit()

    def empty_skill_list(self):
        self.skillsList.clear()
        db.session.commit()

    @classmethod
    def add_skills_to_list(cls, collab, skills) -> None:
        collab.empty_skill_list();
        for skillName in skills:
            skill = SkillsModel.find_by_name(skillName)
            if skill is None:
                skill = SkillsModel(skillName)
                skill.save_to_db()
            skill.collabs.append(collab)
            db.session.commit()

    @classmethod
    def add_classes_to_list(cls, collab, classes) -> None:
        collab.empty_class_list()
        for className in classes:
            course = ClassesModel.find_by_name(className)
            if course is None:
                course = ClassesModel(className)
                course.save_to_db()
            course.collabs.append(collab)
            db.session.commit()

    @classmethod
    def add_member_to_list(cls, collab, user) -> None:
        user.collabs.append(collab)
        db.session.commit()

    @classmethod
    def remove_member_to_list(cls, collab, user) -> None:
        user.collabs.remove(collab)
        db.session.commit()

    @classmethod
    def find_all(cls) -> List["CollabModel"]:
        return cls.query.all()

    @classmethod
    def find_user_collabs(cls, user) -> List["CollabModel"]:
        return cls.query.filter_by(owner=user.email).all()

    @classmethod
    def find_by_id(cls, _id: int) -> "CollabModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_rec_collabs(cls, user) -> List["CollabModel"]:
        knownByUserList = user.skillsList + user.classesList
        knownByUser = dict((rec.name, True) for rec in knownByUserList)
        allCollabs = cls.query.filter(CollabModel.owner != user.email).all()
        joinedCollabs = user.collabsList
        recCollabs = []
        for collab in allCollabs:
            if collab in joinedCollabs:
                continue
            members = collab.membersList
            required = collab.skillsList + collab.classesList
            requiredDict = dict((rec.name, 0) for rec in required)
            for req in required:
                knowReq = req.users
                for member in members:
                    if member in knowReq:
                        requiredDict[req.name] += 1
            thresholdForRating = collab.size/2
            collabRating = 0
            requiredMetCount = 0
            # print(knownByUser)
            # print(requiredDict)
            for key in requiredDict:
                if requiredDict[key] <= thresholdForRating:
                    if knownByUser.get(key, False):
                        collabRating += 1
                else:
                    requiredMetCount += 1
            thresholdForAddingCollab = math.floor((len(requiredDict) - requiredMetCount)/2)
            if collabRating >= thresholdForAddingCollab:
                recCollabs.append(collab)
        return recCollabs

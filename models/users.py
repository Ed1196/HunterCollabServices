from typing import Dict, List, Union
from db import db
from models.classes import ClassesModel, ClassesJSON
from models.skills import SkillsModel, SkillsJSON
from models.collaborations import CollabJSON

# Costume(custom JSON) return type, will help in type hinting
UserJSON = Dict[str, Union[str, str, str, str, List[SkillsJSON], List[ClassesJSON], List[CollabJSON]]]
"""
Association tables that will be the connector in a Many-to-Many relationship between two tables.
    skills: Will associate skills required for a collab to the collabs that have specified them.
    classes: Will associate classes required for a collab to the collabs that have specified them.
    members: Will associate members required for a collab to the collabs that the user has joined 
"""
skills_association = db.Table(
    "user_skills",
    db.Column("user_id", db.Integer, db.ForeignKey("users.id")),
    db.Column("skill_id", db.Integer, db.ForeignKey("skills.id")),
)

classes_association = db.Table(
    "user_classes",
    db.Column("user_id", db.Integer, db.ForeignKey("users.id")),
    db.Column("class_id", db.Integer, db.ForeignKey("classes.id")),
)

collabs_association = db.Table(
    "user_collabs",
    db.Column("user_id", db.Integer, db.ForeignKey("users.id")),
    db.Column("collab_id", db.Integer, db.ForeignKey("collaborations.id")),
)


class UserModel(db.Model):
    """
    A class used to represent an internal representation of a User entity. The UserModel will be a helper file
    that will aid the programmer in development of the API.

    Args
    ----
    db.Model: Model extends db. Lets sqlAlchemy that UserModel will be stored in the database


    Attributes
    ----------
    __tablename__: Name of the table that will be created in the database.
    id: Generates the id for the user
    email: Users username
    password: Users password
    profile_picture: Will store a users profile picture
    skills: Points to the SkillsModel class and loads multiple of those.
    classes: Points to the SkillsModel class and loads multiple of those


    Methods
    -------
    __init__(email, password, github, linkedin, profile_picture, skills, classes)
        Initializes an object of class UserModel. This object will have access to all of its methods
    json()
        Will turn all of UserModel attributes and convert them to json format.
    save_to_db()
        Uses the current session to create a new user in the users table in the db.
    delete_from_db()
        Uses the current session to delete a user from the users table in the db.
    find_my_email()
        Helper method that uses a users email to make a query that will try to find a user with that email.

    """

    # Object properties that will be turned into valid sql queries by SQLAlchemy.
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key="True")
    email = db.Column(db.String(40), unique=True)
    password = db.Column(db.String(40))
    username = db.Column(db.String(40))
    github = db.Column(db.String(40))
    linkedIn = db.Column(db.String(40))
    skillsList = db.relationship(
        "SkillsModel",
        secondary=skills_association,
        backref=db.backref("users", lazy="joined"),
    )
    classesList = db.relationship(
        "ClassesModel",
        secondary=classes_association,
        backref=db.backref("users", lazy="joined"),
    )
    collabsList = db.relationship(
        "CollabModel",
        secondary=collabs_association,
        backref=db.backref("users", lazy="joined")
    )
    profilePicture = None

    def __init__(
            self,
            email: str,
            password: str,
            username: str = "",
            github: str = "",
            linkedIn: str = "",
            profilePicture="",
            skills: List = [],
            classes: List = [],
            collabs: List = [],
    ):
        self.username = username
        self.email = email
        self.password = password
        self.github = github
        self.linkedIn = linkedIn
        self.profilePicture = profilePicture
        self.skills = skills
        self.classes = classes
        self.collabs = collabs

    def json(self) -> UserJSON:
        return {
            "username": self.username,
            "email": self.email,
            "github": self.github,
            "linkedIn": self.linkedIn,
            "profile_picture": self.profilePicture,
            "skills": [skill.name for skill in self.skillsList],
            "classes": [course.name for course in self.classesList],
            "collabs": [collab.json() for collab in self.collabsList],
        }

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()

    def empty_class_list(self):
        self.classesList.clear()
        db.session.commit()

    def empty_skill_list(self):
        self.skillsList.clear()
        db.session.commit()

    @classmethod
    def find_by_email(cls, email: str) -> "UserModel":
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_id(cls, _id: int) -> "UserModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all(cls) -> List["UserModel"]:
        return cls.query.all()

    @classmethod
    def add_skills_to_user(cls, user, skills) -> None:
        for skillName in skills:
            skill = SkillsModel.find_by_name(skillName)
            skill.users.append(user)
            db.session.commit()

    @classmethod
    def add_classes_to_user(cls, user, classes) -> None:
        for className in classes:
            _class = ClassesModel.find_by_name(className)
            _class.users.append(user)
            db.session.commit()

    def add_collab_to_user(self, collab):
        collab.users.append(self)
        db.session.commit()

    def remove_collab_from_user(self, collab):
        collab.users.remove(self)
        db.session.commit()

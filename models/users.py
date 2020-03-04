from db import db
from models.classes import ClassesModel
from models.skills import SkillsModel


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
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key="True")
    email = db.Column(db.String(40))
    password = db.Column(db.String(40))
    github = db.Column(db.String(40))
    linkedin = db.Column(db.String(40))
    profilePicture = None

    # Relationships

    def __init__(self, email, password, github='', linkedin='', profilePicture='', skills=[], classes=[]):
        self.email = email
        self.password = password
        self.github = github
        self.linkedin = linkedin
        self.profilePicture = profilePicture
        self.skills = skills
        self.classes = classes

    def json(self):
        return {
            'email': self.email,
            'github': self.github,
            'linkedin': self.linkedin,
            'profile_picture': self.profilePicture,
            'skills': [skill.json() for skill in self.skills.all()],  # Uses list comprehension to retrieve items
            'classes': [course.json() for course in self.classes.all()]  # Uses list comprehension to retrieve classes

        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

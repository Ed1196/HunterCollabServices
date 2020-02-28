from db import db


class ClassesModel(db.Model):
    __tablename__ = 'classes'
    classes_name = db.Column(db.String(40))
    user_id = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=False)

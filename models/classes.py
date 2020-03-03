from db import db


class ClassesModel(db.Model):
    __tablename__ = 'classes'
    id = db.Column(db.Integer, primary_key="True")
    classes_name = db.Column(db.String(40))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

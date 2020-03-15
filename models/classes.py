from db import db


class ClassesModel(db.Model):
    __tablename__ = 'classes'
    id = db.Column(db.Integer, primary_key="True")
    name = db.Column(db.String(40), unique=True)

    def __init__(self, className):
        self.name = className

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()


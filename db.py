from flask_sqlalchemy import SQLAlchemy

"""
Attributes
----------
db: SQLAlchemy
    Object that will link to the flask app. It will look for models that were declared with the db object.
    This initializes the SQLAlchemy Object Relational Mapper. 
"""
db = SQLAlchemy()
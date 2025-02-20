    
from database import db

class User(db.Model):
    __tablename__ = 'users'  # Explicitly match the table name
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)  # Username must be unique
    password = db.Column(db.String(120), nullable=False)


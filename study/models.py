from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy.orm import relationship

db = SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    name = db.Column(db.String(200))
    bio = db.Column(db.Text)
    avatar = db.Column(db.String(200), default='avatar.svg')
    password = db.Column(db.String(150), nullable=False)

    # Relationships
    rooms_hosted = db.relationship('Room', backref='host', lazy=True, foreign_keys='Room.host_id')
    rooms_participated = db.relationship('Room', secondary='room_participants', backref='participants', lazy='dynamic')

    def __repr__(self):
        return f'<User {self.username}>'

class Topic(db.Model):
    __tablename__ = 'topic'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'<Topic {self.name}>'

class Room(db.Model):
    __tablename__ = 'room'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    updated = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
    created = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)
    
    host_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'), nullable=True)
    
    # Relationships
    host = db.relationship('User', back_populates='rooms_hosted')
    topic = db.relationship('Topic')
    
    def __repr__(self):
        return f'<Room {self.name}>'

class Message(db.Model):
    __tablename__ = 'message'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    body = db.Column(db.Text, nullable=False)
    updated = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
    created = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)
    
    user = db.relationship('User', backref='messages')
    room = db.relationship('Room', backref='messages')
    
    def __repr__(self):
        return f'<Message {self.body[:50]}>'

# Association table for Room and User many-to-many relationship
room_participants = db.Table('room_participants',
    db.Column('room_id', db.Integer, db.ForeignKey('room.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
)

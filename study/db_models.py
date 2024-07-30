from datetime import *
from . import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    username = db.Column(db.String(50), primary_key=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    profile = db.relationship('Profile', back_populates='user', uselist=False, cascade="all, delete-orphan")
    groups = db.relationship('GroupMember', back_populates='user', cascade="all, delete-orphan")

    def get_id(self):
        return self.username

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"
    
class Profile(db.Model):
    __tablename__ = 'profile'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), db.ForeignKey('user.username', ondelete='CASCADE', onupdate='CASCADE', name='fk_profile_user_username'), nullable=False)
    school = db.Column(db.String(100), nullable=False)
    strong_subjects = db.Column(db.String(255), nullable=False)
    weak_subjects = db.Column(db.String(255), nullable=False)
    primary_language = db.Column(db.String(50), nullable=False)
    secondary_languages = db.Column(db.String(200))
    days = db.Column(db.String(50), nullable=False)
    times = db.Column(db.String(50), nullable=False)

    user = db.relationship('User', back_populates='profile')

class Group(db.Model):
    __tablename__ = 'group'
    id = db.Column(db.Integer,  primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    days = db.Column(db.String(50), nullable=False)
    times = db.Column(db.String(50), nullable=False)
    creator = db.Column(db.String(50), db.ForeignKey('user.username', ondelete='CASCADE', onupdate='CASCADE', name='fk_group_user_username'), nullable=False)
    members = db.relationship('GroupMember', back_populates='group', cascade="all, delete-orphan")

class GroupMember(db.Model):
    __tablename__ = 'group_members'
    group_id = db.Column(db.Integer, db.ForeignKey('group.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    user_id = db.Column(db.String(50), db.ForeignKey('user.username', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    
    group = db.relationship('Group', back_populates='members')
    user = db.relationship('User', back_populates='groups')

class Review(db.Model):
    _tablename_ = 'reviews'
    id = db.Column(db.Integer,  primary_key=True, autoincrement=True)
    message = db.Column(db.String(1024),nullable = False)
    rating = db.Column(db.Integer,nullable = False)
    userto = db.Column(db.String(50),nullable = False)
    userfrom = db.Column(db.String(50),nullable = False)    

class Event(db.Model):
    __tablename__ = 'event'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    summary = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    start_datetime = db.Column(db.DateTime, nullable=False)
    end_datetime = db.Column(db.DateTime, nullable=False)
    meet_link = db.Column(db.String(255))
    group_id = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, summary,  description, start_datetime, end_datetime, meet_link, group_id):
        self.summary = summary
        self.description = description
        self.start_datetime = start_datetime
        self.end_datetime = end_datetime
        self.meet_link = meet_link
        self.group_id = group_id
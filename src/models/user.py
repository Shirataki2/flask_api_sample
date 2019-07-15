from database.db import db
from .post import PostModel
from sqlalchemy import desc

followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('users.id'))
)

class UserModel(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(256), nullable=False)
    password = db.Column(db.String(1024), nullable=False)
    posts = db.relationship(PostModel, backref='users')
    followed = db.relationship(
        'UserModel',
        secondary=followers,
        primaryjoin=(followers.c.follower_id==id),
        secondaryjoin=(followers.c.followed_id==id),
        backref=db.backref('followers', lazy='dynamic'),
        lazy='dynamic'
    )
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def json(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email
        }, 200

    def get_posts(self, limit, offset):
        return PostModel.query.order_by(desc(PostModel.id)).limit(limit).offset(offset)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def remove_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_user_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_user_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def get_all_users(cls):
        return cls.query.all()

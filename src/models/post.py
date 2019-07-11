from database.db import db
from datetime import datetime
from sqlalchemy_utils import UUIDType
import uuid


class PostModel(db.Model):
    __tablename__ = "posts"
    id = db.Column(
        db.Integer,
        primary_key=True,
    )
    uid = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False
    )
    text = db.Column(db.String(240), nullable=False)
    post_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )
    def __init__(self, text):
        self.text = text

    def json(self):
        return {
            "id": self.id,
            "user_id": self.uid,
            "text": self.text
        }, 200

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def remove_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_posts_by_post_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

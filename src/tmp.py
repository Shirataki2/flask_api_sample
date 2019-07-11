from app import create_app
from database.db import db
from models.post import PostModel
from models.user import UserModel


app = create_app('TEST')
with app.app_context():
    db.drop_all()
    db.create_all()
    db.session.commit()
    u = UserModel('diof', 'hashed')
    p = PostModel('wdowdenwof')
    u.posts.append(p)
    db.session.add(p)
    p = PostModel('ewpofjwo[w')
    u.posts.append(p)
    db.session.add(p)
    p = PostModel('ewpkwmfe')
    u.posts.append(p)
    db.session.add(p)
    db.session.add(u)
    u = UserModel('fipehw', 'fejwpi')
    p = PostModel('efjpiwf')
    u.posts.append(p)
    db.session.add(p)
    db.session.add(u)
    db.session.commit()
    for user in db.session.query(UserModel).all():
        print(user.id, user.username)
        for post in user.posts:
            print('\t', post.id, post.uid, post.text)


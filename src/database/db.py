from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()

def init_db(app):
    db.init_app(app)
    print(db)
    Migrate(app, db)

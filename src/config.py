import os

class DevConfig:
    # Flask
    DEBUG = True
    # SQLAlchemy
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://%s:%s@%s/%s?charset=utf8' % (
        os.getenv('DB_USER', 'root'),
        os.getenv('DB_PASSWORD', ''),
        os.getenv('DB_HOST', 'localhost'),
        os.getenv('DB_NAME', 'flasksqlalchemy')
    )
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class TestConfig:
    # Flask
    DEBUG = True
    # SQLAlchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://%s:%s@%s/%s?charset=utf8' % (
        os.getenv('DB_USER', 'root'),
        os.getenv('DB_PASSWORD', 'V@nhouten530'),
        os.getenv('DB_HOST', 'localhost'),
        os.getenv('TEST_DB_NAME', 'test_flask_social')
    )
    SQLALCHEMY_ECHO = False

class ProdConfig:
    # Flask
    DEBUG = False
    # SQLAlchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://%s:%s@%s/%s?charset=utf8' % (
        os.getenv('DB_USER', 'root'),
        os.getenv('DB_PASSWORD', ''),
        os.getenv('DB_HOST', 'localhost'),
        os.getenv('DB_NAME', 'flasksqlalchemy')
    )
    SQLALCHEMY_ECHO = False

env = os.getenv('ENV', 'DEV')

if env == 'DEV':
    Config = DevConfig
elif env == 'TEST':
    Config = TestConfig
else:
    Config = ProdConfig


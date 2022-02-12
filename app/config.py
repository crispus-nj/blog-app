import os
class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
class ProdConfig(Config):
    pass
class DevConfig(Config):
    DEBUG = True
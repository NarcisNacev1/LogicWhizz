class Config:
     SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:narcis1@localhost:5432/logicwizz_be'
    #SQLALCHEMY_DATABASE_URI = 'postgresql://<username>:<password>@<host>:<port>/<database>'
     SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

class TestingConfig(Config):
    DEBUG = True
    TESTING = True
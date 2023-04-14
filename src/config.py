
class DevelopmentConfig():
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:190319@localhost/proyect2'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
config = {
    'development': DevelopmentConfig
}



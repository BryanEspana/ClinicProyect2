class DevelopmentConfig():
    DEBUG = True
    endpoint = 'proyecto2-db1.cd5zvwqtmiac.us-east-2.rds.amazonaws.com'
    username = 'postgres'
    password = 'BryanJavierSebas'
    database_name = 'CentroMedico'
    port = '5432'
    SQLALCHEMY_DATABASE_URI = 'postgresql://{username}:{password}@{endpoint}:{port}/{database_name}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
config = {
    'development': DevelopmentConfig
}
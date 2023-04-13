class DevelopmentConfig():
    DEBUG = True
    MYSQL_HOST = 'db1proyecto.cd5zvwqtmiac.us-east-2.rds.amazonaws.com'
    MYSQL_USER = 'admin'
    MYSQL_PASSWORD = 'BryanJavierSebas'
    MYSQL_DB = 'tubasededatos'

config = {
    'development': DevelopmentConfig
}

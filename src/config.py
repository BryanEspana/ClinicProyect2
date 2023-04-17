import secrets

import subprocess
import sys

def install_package(package):
    """Instala un paquete utilizando pip"""
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def check_module(package):
    """Verifica si un módulo está instalado y, en caso contrario, lo instala"""
    try:
        __import__(package)
    except ImportError:
        print(f"{package} no está instalado. Instalando ahora...")
        install_package(package)

check_module('secrets')

secret_key = secrets.token_hex(32)

class DevelopmentConfig():
    DEBUG = True
    endpoint = 'proyecto2-db1.cd5zvwqtmiac.us-east-2.rds.amazonaws.com'
    username = 'postgres'
    password = 'BryanJavierSebas'
    database_name = 'CentroMedico'
    port = '5432'
    SQLALCHEMY_DATABASE_URI = f'postgresql://{username}:{password}@{endpoint}:{port}/{database_name}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = secrets.token_hex(32)

    
config = {
    'development': DevelopmentConfig
}
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    # Elimina la configuración existente de la base de datos para evitar conflictos
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') 
    # SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = os.environ.get('DEBUG') or True

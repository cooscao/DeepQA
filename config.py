import os

basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True

SECRET_KEY = os.urandom(24)
HOSTNAME = '127.0.0.1'
PORT = 3306
DATABASE = 'deepqa'
USERNAME = 'root'
PASSWORD = 'cs19960406'
DB_URI = 'mysql+mysqldb://{}:{}@{}:{}/{}'.format(USERNAME, PASSWORD,
                                                HOSTNAME, PORT, DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = True 
SQLALCHEMY_COMMIT_ON_TEARDOWN = True              
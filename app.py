from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'planets.db')
db = SQLAlchemy()
db.init_app(app)

from routes import *
from models import *

if __name__ == '__main__':
  app.debug = True
  app.run()
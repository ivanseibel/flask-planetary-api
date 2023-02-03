from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'planets.db')

db = SQLAlchemy(app)


# Routes

@app.route('/')
def hello_world():
  # Gets user name that comes from the request
  name = request.args.get('name')
  
  # If user name is not provided, return a message
  if name is None:
    return jsonify({'message': 'Please provide a name'})

  # If user name is provided, return a message
  return jsonify({'message': f'Hello {name}'})


@app.route('/parameters')
def parameters():
  age = int(request.args.get('age'))
  name = request.args.get('name')

  if age < 18:
    return ({
      'message': f'Sorry {name}, you are not old enough to view this page'
    }), 401

  return ({
    'message': f'Welcome {name}, you are old enough to view this page'
  })


@app.route('/url_variables/<string:name>/<int:age>')
def url_variables(name: str, age: int):
  if age < 18:
    return ({
      'message': f'Sorry {name}, you are not old enough to view this page'
    }), 401

  return ({
    'message': f'Welcome {name}, you are old enough to view this page'
  })


# Database Models

class User(db.Model):
  __tablename__ = 'users'
  id = Column(Integer, primary_key=True)
  first_name = Column(String)
  last_name = Column(String)
  email = Column(String, unique=True)
  password = Column(String)


class Planet(db.Model):
  __tablename__ = 'planets'
  planet_id = Column(Integer, primary_key=True)
  planet_name = Column(String)
  planet_type = Column(String)
  home_star = Column(String)
  mass = Column(Float)
  radius =  Column(Float)
  distance = Column(Float)


if __name__ == '__main__':
  app.run()
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flaskalchemy import Column, Integer, String, Float
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'planets.db')

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


if __name__ == '__main__':
  app.run()
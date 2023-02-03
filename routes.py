from flask import Flask, jsonify, request
from app import app

@app.route('/')
def hello_world():
  name = request.args.get('name')
  if name is None:
    return jsonify({'message': 'Please provide a name'})
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

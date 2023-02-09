from flask import Flask, jsonify, request
from app import app, mail
from models import *
from flask_jwt_extended import create_access_token
from flask_mail import Message

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


@app.route('/planets', methods=['GET'])
def planets():
  planets_list = Planet.query.all()

  result = planets_schema.dump(planets_list)

  return jsonify(result)


@app.route('/register', methods=['POST'])
def register():
  email = request.form['email']

  test_email = User.query.filter_by(email=email).first()

  if test_email:
    return jsonify({'message': 'Email already exists'}), 409

  first_name = request.form['first_name']
  last_name = request.form['last_name']
  password = request.form['password']

  user = User(
    first_name=first_name,
    last_name=last_name,
    email=email,
    password=password
  )

  db.session.add(user)

  db.session.commit()

  return jsonify({'message': 'User created successfully'}), 201


@app.route('/login', methods=['POST'])
def login():
  if request.is_json:
    email = request.json['email']
    password = request.json['password']
  else:
    email = request.form['email']
    password = request.form['password']

  user = User.query.filter_by(email=email, password=password).first()

  if user:
    access_token = create_access_token(identity=email)
    return jsonify({'message': 'Login successful', 'access_token': access_token})
  else:
    return jsonify({'message': 'Bad email or password'}), 401


@app.route('/retrieve_password/<string:email>', methods=['GET'])
def retrieve_password(email: str):
  user = User.query.filter_by(email=email).first()

  if user:
    msg = Message(
      'Your planetary API password is ' + user.password,
      sender="admin@planetary-api.com",
      recipients=[email]
    )
    mail.send(msg)
    return jsonify({'message': 'Password sent to ' + email})
  else:
    return jsonify({'message': 'Email does not exist'}), 401


# Retrieving a single planet's details
@app.route('/planets/<int:planet_id>', methods=['GET'])
def planet_details(planet_id: int):
  planet = Planet.query.filter_by(planet_id=planet_id).first()

  if planet:
    result = planet_schema.dump(planet)
    return jsonify(result)
  else:
    return jsonify({'message': 'Planet does not exist'}), 404
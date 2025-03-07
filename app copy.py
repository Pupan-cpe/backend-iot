from flask import Flask, request, jsonify, make_response
from config.config import DB_URL
from model.users import User, IotDevice, db


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
db.init_app(app)

with app.app_context():
    db.create_all()

# create a test route


@app.route('/test', methods=['GET'])
def test():
    return make_response(jsonify({'message': 'test route'}), 200)

# create a user


@app.route('/iot-pw', methods=['POST'])
def iotData():
    try:
        data = request.get_json()
        new_data = IotDevice(device=data['device'], device_no=data['device_no'], status=data['status'], isActive=data['isActive'],
                             event=data['event'], created_by=data['created_by'],)
        db.session.add(new_data)
        db.session.commit()
        return make_response(jsonify({'message': 'iot created'}), 201)
    except Exception as e:
        return make_response(jsonify({'message': 'error creating iot', 'error': str(e)}), 500)

# create a user


@app.route('/users', methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        new_user = User(username=data['username'], email=data['email'])
        db.session.add(new_user)
        db.session.commit()
        return make_response(jsonify({'message': 'user created'}), 201)
    except e:
        return make_response(jsonify({'message': 'error creating user'}), 500)


# get all users
@app.route('/users', methods=['GET'])
def get_users():
    try:
        users = User.query.all()
        return make_response(jsonify([user.json() for user in users]), 200)
    except e:
        return make_response(jsonify({'message': 'error getting users'}), 500)


# get a user by id
@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    try:
        user = User.query.filter_by(id=id).first()
        if user:
            return make_response(jsonify({'user': user.json()}), 200)
        return make_response(jsonify({'message': 'user not found'}), 404)
    except e:
        return make_response(jsonify({'message': 'error getting user'}), 500)


# update a user
@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    try:
        user = User.query.filter_by(id=id).first()
        if user:
            data = request.get_json()
            user.username = data['username']
            user.email = data['email']
            db.session.commit()
            return make_response(jsonify({'message': 'user updated'}), 200)
        return make_response(jsonify({'message': 'user not found'}), 404)
    except e:
        return make_response(jsonify({'message': 'error updating user'}), 500)


# delete a user
@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    try:
        user = User.query.filter_by(id=id).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            return make_response(jsonify({'message': 'user deleted'}), 200)
        return make_response(jsonify({'message': 'user not found'}), 404)
    except e:
        return make_response(jsonify({'message': 'error deleting user'}), 500)

from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import bcrypt
from models import db, User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or not all(k in data for k in ('name', 'email', 'password')):
        return jsonify({'error': 'name, email and password are required'}), 400
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already registered'}), 409
    hashed = bcrypt.hashpw(data['password'].encode(), bcrypt.gensalt()).decode()
    user = User(name=data['name'], email=data['email'], password_hash=hashed,
                phone=data.get('phone'), address=data.get('address'))
    db.session.add(user)
    db.session.commit()
    token = create_access_token(identity=str(user.user_id), additional_claims={'role': user.role})
    return jsonify({'token': token, 'user': user.to_dict()}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not all(k in data for k in ('email', 'password')):
        return jsonify({'error': 'email and password required'}), 400
    user = User.query.filter_by(email=data['email']).first()
    if not user or not bcrypt.checkpw(data['password'].encode(), user.password_hash.encode()):
        return jsonify({'error': 'Invalid credentials'}), 401
    token = create_access_token(identity=str(user.user_id), additional_claims={'role': user.role})
    return jsonify({'token': token, 'user': user.to_dict()})

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def me():
    user = User.query.get(int(get_jwt_identity()))
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user.to_dict())

@auth_bp.route('/me', methods=['PUT'])
@jwt_required()
def update_profile():
    user = User.query.get(int(get_jwt_identity()))
    data = request.get_json()
    for field in ('name', 'phone', 'address'):
        if field in data:
            setattr(user, field, data[field])
    db.session.commit()
    return jsonify(user.to_dict())

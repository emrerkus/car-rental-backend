from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from app.models import User
from app.db import db
from app.auth import auth

bp = Blueprint('auth', __name__)


# This function allows registering on the platform
@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    role = data.get('role')

    if not username or not password or not role:
        return jsonify({"ERROR": "Missing Information"}), 400
    if role not in ['user', 'merchant', 'admin']:
        return jsonify({"ERROR": "Invalid User Type"}), 400
    if User.query.filter_by(username=username).first():
        return jsonify({"ERROR": "This Username is Taken"}), 409

    hashed_pw = generate_password_hash(password)
    new_user = User(username=username, password=hashed_pw, role=role)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"MESSAGE": "Registration Successful!",
                    "Your Username": username,
                    "Your Role": role}), 201


# This function can be used to authenticate the user
@auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        return user
    return None

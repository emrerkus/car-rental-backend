from flask import Blueprint, request, jsonify
from app import db
from app.auth import auth
from app.models import Rental, Car, User

bp = Blueprint('admin', __name__)


@bp.route('/users', methods=['GET'])
@auth.login_required
def get_users():
    current_user = auth.current_user()
    if current_user.username == "admin":
        users = User.query.all()

        return jsonify([{
            "User ID": user.id,
            "Username": user.username,
            "User Role": user.role
        } for user in users]), 200

    return jsonify({"ERROR": "This is only for admin"}), 200


@bp.route('/cars/<int:user_id>', methods=['GET'])
@auth.login_required
def get_cars_for_any_user(user_id):
    current_user = auth.current_user()
    if current_user.username == "admin":
        cars = Car.query.filter_by(merchant_id=user_id)
        return jsonify([{
            "Car ID": car.id,
            "Car Title": car.name,
            "Car Availability": car.available,
            "Car Brand": car.brand,
            "Car Color": car.color,
            "Car Engine": car.engine,
            "Car Type": car.car_type
        } for car in cars]), 200
    return jsonify({"ERROR": "Only admin can access this link"})

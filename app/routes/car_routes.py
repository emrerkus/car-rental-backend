from flask import Blueprint, request, jsonify
from app.models import Car
from app.db import db
from app.auth import auth

bp = Blueprint('car', __name__)


# It allows registered users to view all cars on the platform with filtering feature
@bp.route('/cars', methods=['GET'])
@auth.login_required
def get_all_cars():
    my_query = Car.query.filter(Car.available == True)

    brand = request.args.get('brand')
    color = request.args.get('color')
    engine = request.args.get('engine', type=float)
    car_type = request.args.get('car_type')

    if brand:
        my_query = my_query.filter(Car.brand == brand)
    if color:
        my_query = my_query.filter(Car.color == color)
    if engine:
        my_query = my_query.filter(Car.engine == engine)
    if car_type:
        my_query = my_query.filter(Car.car_type == car_type)

    cars = my_query.all()

    return jsonify([{
        "Car ID": car.id,
        "Car Title": car.name,
        "Car Availability": car.available,
        "Car Brand": car.brand,
        "Car Color": car.color,
        "Car Engine": car.engine,
        "Car Type": car.car_type
    } for car in cars]), 200


# It allows users with the merchant role to see the vehicles they have uploaded to the platform
@bp.route('/profile/my-cars', methods=['GET'])
@auth.login_required
def get_my_cars():
    user = auth.current_user()
    if user.role == 'user':
        return jsonify({"ERROR": "Only users with the merchant role can access this link"}), 403

    cars = Car.query.filter_by(merchant_id=user.id).all()

    return jsonify([{
        "Car ID": car.id,
        "Car Title": car.name,
        "Car Availability": car.available,
        "Car Brand": car.brand,
        "Car Color": car.color,
        "Car Engine": car.engine,
        "Car Type": car.car_type
    } for car in cars]), 200


# It allows users with the merchant role to add new vehicles to the platform
@bp.route('/profile/my-cars', methods=['POST'])
@auth.login_required
def add_car():
    user = auth.current_user()
    if user.role != "merchant":
        return jsonify({"ERROR": "Only users with the merchant role can add new vehicles."}), 403

    data = request.get_json()
    name = data.get('name')
    brand = data.get('brand')
    color = data.get('color')
    engine = data.get('engine')
    car_type = data.get('car_type')
    merchant_id = user.id
    if not name:
        return jsonify({"ERROR": "Vehicle name not entered"}), 400
    if not brand:
        return jsonify({"ERROR": "Vehicle brand not entered"}), 400
    if not color:
        return jsonify({"ERROR": "Vehicle color not entered"}), 400
    if not engine:
        return jsonify({"ERROR": "Vehicle engine not entered"}), 400
    if not car_type:
        return jsonify({"ERROR": "Vehicle type not entered"}), 400

    car = Car(name=name, merchant_id=merchant_id, brand=brand, color=color, engine=engine, car_type=car_type)
    db.session.add(car)
    db.session.commit()
    return jsonify({"MESSAGE": "Your car has been added to the platform successfully"}), 201


# Allows users with the merchant role to edit their vehicle uploaded to the platform
@bp.route('/profile/my-cars/<int:car_id>', methods=['PATCH'])
@auth.login_required
def update_car(car_id):
    user = auth.current_user()
    car = Car.query.get(car_id)

    if not car:
        return jsonify({"ERROR": "Vehicle not found"}), 404

    if not car.available:
        return jsonify({"ERROR": "This vehicle is currently on loan. It can be arranged upon return"}), 403

    if car.merchant_id != user.id:
        return jsonify({"ERROR": "You do not have permission to access this vehicle"}), 403

    data = request.get_json()

    if 'name' in data:
        car.name = data['name']
    if 'brand' in data:
        car.brand = data['brand']
    if 'color' in data:
        car.color = data['color']
    if 'engine' in data:
        car.engine = data['engine']
    if 'car_type' in data:
        car.car_type = data['car_type']

    db.session.commit()

    return jsonify({
        "MESSAGE": "The vehicle has been updated successfully",
    }), 200


# Allows users with the merchant role to delete their vehicle uploaded to the platform
@bp.route('/profile/my-cars/<int:car_id>', methods=['DELETE'])
@auth.login_required
def delete_car(car_id):
    user = auth.current_user()
    car = Car.query.get(car_id)
    if not car:
        return jsonify({"ERROR": "There is no such vehicle on the platform"}), 404

    if not car.available:
        return jsonify({"ERROR": "This vehicle is currently on loan. It may be deleted upon return"}), 403

    if user.id == car.merchant_id:
        db.session.delete(car)
        db.session.commit()
        return jsonify({"MESSAGE": "Vehicle deleted successfully"}), 200
    else:
        return jsonify({"ERROR": "There is no such vehicle."}), 404

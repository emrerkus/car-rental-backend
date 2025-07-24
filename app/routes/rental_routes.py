from datetime import datetime
from flask import Blueprint, request, jsonify
from app import db
from app.auth import auth
from app.models import Rental, Car

bp = Blueprint('rental', __name__)


# It enables users with the user role to rent available vehicles on the platform
@bp.route('/rent', methods=['POST'])
@auth.login_required
def rent_car():
    user = auth.current_user()
    if user.role != 'user':
        return jsonify({"ERROR": "Only users with the user role can rent a car"}), 403

    data = request.get_json()
    car_id = data.get('car_id')

    car = Car.query.get(car_id)
    if not car:
        return jsonify({"ERROR": "Vehicle not found"}), 404
    if not car.available:
        return jsonify({"ERROR": "This vehicle is currently unavailable"}), 400
    filtered_rentals = Rental.query.filter_by(user_id=user.id)
    for rental in filtered_rentals:
        if rental.end_date is None:
            return jsonify({"ERROR": "You can only rent one vehicle at a time"}), 403

    rental = Rental(user_id=user.id, car_id=car.id, merchant_id=car.merchant_id)
    car.available = False
    db.session.add(rental)
    db.session.commit()

    return jsonify({"MESSAGE": "Vehicle successfully rented", "Rental ID": rental.id}), 201


# It's a two-side function.
# It allows users with the merchant role to see the vehicles they've given,
# while users with the use role can see the vehicles they've rented.
@bp.route('/profile/rentals', methods=['GET'])
@auth.login_required
def get_my_rentals():
    user = auth.current_user()

    rentals = None
    if user.role == "user":
        rentals = Rental.query.filter_by(user_id=user.id).all()
    elif user.role == "merchant":
        rentals = Rental.query.filter_by(merchant_id=user.id).all()

    result = []
    for rental in rentals:
        result.append({
            "Rental ID": rental.id,
            "Car ID": rental.car_id,
            "User ID": rental.user_id,
            "Merchant ID": rental.merchant_id,
            "Start Date": rental.start_date.strftime("%d-%m-%Y %H:%M:%S"),
            "End Date": rental.end_date.strftime("%d-%m-%Y %H:%M:%S") if rental.end_date else None
        })

    return jsonify(result), 200


# Allows users with the user role to return the vehicles they rented
@bp.route('/return/<int:rental_id>', methods=['POST'])
@auth.login_required
def return_car(rental_id):
    user = auth.current_user()

    if user.role != "user":
        return jsonify({"ERROR": "Only users with the user role can return the vehicle"}), 403

    rental = Rental.query.get(rental_id)

    if not rental:
        return jsonify({"ERROR": "No rental record found"}), 404

    if rental.user_id != user.id:
        return jsonify({"ERROR": "This rental does not belong to you"}), 403

    if rental.end_date:
        return jsonify({"MESSAGE": "This vehicle has already been returned"}), 400

    rental.end_date = datetime.utcnow()

    car = Car.query.get(rental.car_id)
    car.available = True

    db.session.commit()

    total_time = rental.end_date - rental.start_date
    total_price = total_time.total_seconds() / 3600 * car.price_per_hour

    return jsonify({
        "MESSAGE": f"Vehicle successfully returned, total time: {total_time}",
        "Rental ID": rental.id,
        "Return Date": rental.end_date.strftime("%d-%m-%Y %H:%M:%S"),
        "Total Payment": total_price
    }), 200

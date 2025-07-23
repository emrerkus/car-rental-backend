from flask import Blueprint, jsonify, request
from app.auth import auth
from app.db import db
from app.models import Rental, Car

bp = Blueprint('user', __name__)


# This function allows the user to view his/her personal information
@bp.route('/profile', methods=['GET'])
@auth.login_required
def get_me():
    user = auth.current_user()
    return jsonify({
        "Your User ID": user.id,
        "Your Username": user.username,
        "Your Role": user.role
    }), 200


@bp.route('/profile', methods=['DELETE'])
@auth.login_required
def delete_me():
    user = auth.current_user()
    active_renter = Rental.query.filter_by(user_id=user.id, end_date=None).first()
    active_lender = Rental.query.filter_by(merchant_id=user.id, end_date=None).first()

    if active_lender or active_renter:
        return jsonify({"ERROR": "Your account contains rental history. It cannot be deleted."}), 403

    db.session.delete(user)
    db.session.commit()
    return jsonify({"MESSAGE": "Account deleted successfully"}), 200

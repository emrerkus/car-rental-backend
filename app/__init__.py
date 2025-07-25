from flask import Flask
from app.db import db
from app.routes import auth_routes, car_routes, user_routes, rental_routes, admin_routes


def create_app(username, password, database_port, database_name):
    app = Flask(__name__)

    # Connects database to the flask app
    app.config[
        'SQLALCHEMY_DATABASE_URI'] = f'postgresql://{username}:{password}@localhost:{database_port}/{database_name}'
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:3406@localhost:5432/testdb'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    app.register_blueprint(auth_routes.bp)
    app.register_blueprint(car_routes.bp)
    app.register_blueprint(user_routes.bp)
    app.register_blueprint(rental_routes.bp)
    app.register_blueprint(admin_routes.bp)

    return app

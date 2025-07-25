from app import create_app
from app.db import db
from app.models import User
from werkzeug.security import generate_password_hash
import sys


username = None
password = None
database_port = None
database_name = None


if __name__ == '__main__':
    if len(sys.argv) != 5:
        print("Usage: python run.py <username> <password> <database_port> <database_name>")
        sys.exit(1)

    username = sys.argv[1]
    password = sys.argv[2]
    database_port = sys.argv[3]
    database_name = sys.argv[4]
    app = create_app(username, password, database_port, database_name)

    with app.app_context():
        db.create_all()
        admin_user = User.query.filter_by(username='admin').first()
        if not admin_user:
            new_admin = User(
                username='admin',
                password=generate_password_hash('admin123'),
                role='admin'
            )
            db.session.add(new_admin)
            db.session.commit()
            print("Admin has been created")
        else:
            print("ERROR")

    app.run(debug=True)

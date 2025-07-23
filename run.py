from app import create_app
from app.db import db
from app.models import User
from werkzeug.security import generate_password_hash

app = create_app()

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

if __name__ == '__main__':
    app.run(debug=True)

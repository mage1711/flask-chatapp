from app import db, loginManager
from flask_login import UserMixin


@loginManager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __reper__(self):
        return f"User('{self.username}','{self.password}')"

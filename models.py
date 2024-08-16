from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

database_path = os.environ.get('DATABASE_URL', 'sqlite:///my_database.db')

db = SQLAlchemy()

def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()

class APIRoute(db.Model):
    __tablename__ = 'api_routes'

    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(128), nullable=False)
    method = db.Column(db.String(10), nullable=False)
    description = db.Column(db.String(255))

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'path': self.path,
            'method': self.method,
            'description': self.description
        }

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    hashed_password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'username': self.username,
            'is_admin': self.is_admin
        }

class AccessLog(db.Model):
    __tablename__ = 'access_logs'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    route_id = db.Column(db.Integer, db.ForeignKey('api_routes.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    status_code = db.Column(db.Integer, nullable=False)
    user = db.relationship('User', backref=db.backref('access_logs', lazy=True))
    route = db.relationship('APIRoute', backref=db.backref('access_logs', lazy=True))

    def insert(self):
        db.session.add(this)
        db.session.commit()

    def delete(self):
        db.session.delete(this)
        db.session.commit()

    def update(self):
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'route_id': self.route_id,
            'timestamp': self.timestamp.isoformat(),
            'status_code': self.status_code
        }
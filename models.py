from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_security import SQLAlchemyUserDatastore, UserMixin, RoleMixin

db = SQLAlchemy()
migrate = Migrate()

roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(10), unique=True)
    password = db.Column(db.String(255))
    helper_id = db.Column(db.Integer,db.ForeignKey('helper.id'))
    active = db.Column(db.Boolean())
    roles = db.relationship('Role', secondary=roles_users,
            backref=db.backref('users', lazy='dynamic'))

class Helper(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(25), unique=True)
    lastname = db.Column(db.String(25), unique=True)
    email = db.Column(db.String(50), unique=True)
    user=db.relationship('User',backref='helper',uselist=False)

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
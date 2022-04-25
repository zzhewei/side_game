###########
# reference:https://www.maxlist.xyz/2019/10/30/flask-sqlalchemy/
#           https://blog.csdn.net/weixin_42677653/article/details/106154452
#           https://dboyliao.medium.com/python-%E7%B9%BC%E6%89%BF-543-bc3d8ef51d6d
#           https://medium.com/bryanyang0528/python-setter-%E5%92%8C-getter-6c08a9d37d46
###########
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from flask_login import UserMixin
from flask import jsonify
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()
migrate = Migrate()


class Permission:
    READ = 1
    WRITE = 2
    MODIFY = 4
    ADMIN = 8


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0

    @staticmethod
    def insert_roles():
        roles = {
            'User': [Permission.READ],
            'Moderator': [Permission.READ, Permission.WRITE, Permission.MODIFY],
            'Administrator': [Permission.READ, Permission.WRITE, Permission.MODIFY, Permission.ADMIN],
        }
        default_role = 'User'
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.reset_permissions()
            for perm in roles[r]:
                role.add_permission(perm)
            role.default = (role.name == default_role)
            db.session.add(role)
        db.session.commit()

    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm

    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm

    def reset_permissions(self):
        self.permissions = 0

    def has_permission(self, perm):
        return self.permissions & perm == perm

    def __repr__(self):
        return '<Role %r>' % self.name


# MRO and C3 Linearization
class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    username = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(200))

    def __init__(self, **kwargs):
        # can write super(User, self).__init__(**kwargs) --> python2
        super().__init__(**kwargs)
        if self.role is None:
            self.role = Role.query.filter_by(default=True).first()

    # property set method only read
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_json(self):
        return {'id': self.id, 'username': self.username}

    def can(self, perm):
        return self.role is not None and self.role.has_permission(perm)

    def is_administrator(self):
        return self.can(Permission.ADMIN)


# 紀錄
class Record(db.Model):
    __tablename__ = 'record'
    rid = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, db.ForeignKey('user.id'))
    rank = db.Column(db.Integer, nullable=False)
    point = db.Column(db.Integer, nullable=False)
    insert_time = db.Column(db.DateTime, default=datetime.now)
    insert_user = db.Column(db.Integer, nullable=False)
    update_time = db.Column(db.DateTime, onupdate=datetime.now, default=datetime.now)
    update_user = db.Column(db.Integer, nullable=False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


def select(SqlContent, *args):
    data = db.session.execute(SqlContent, args)
    db.session.commit()
    return data.mappings().all()


def sqlOP(SqlContent, **args):
    try:
        db.session.execute(SqlContent, args)
        db.session.commit()
    except:
        db.session.rollback()


def return_format(code=200, success=True, data=None):
    if data is None:
        data = {"messages": "success"}
    return jsonify({"code": code, "success": success, "data": data})

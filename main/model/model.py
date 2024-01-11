###########
# reference:https://www.maxlist.xyz/2019/10/30/flask-sqlalchemy/
#           https://blog.csdn.net/weixin_42677653/article/details/106154452
#           https://dboyliao.medium.com/python-%E7%B9%BC%E6%89%BF-543-bc3d8ef51d6d
#           https://medium.com/bryanyang0528/python-setter-%E5%92%8C-getter-6c08a9d37d46
###########
import time

import mongoengine.fields as fields
from flask import jsonify
from flask_mongoengine import MongoEngine
from werkzeug.security import check_password_hash, generate_password_hash

db = MongoEngine()


def return_format(code=200, success=True, data=None):
    if data is None:
        data = {"messages": "success"}
    return jsonify({"code": code, "success": success, "data": data})


# TODO 用大寫就關聯不到 待查
class users(db.Document):
    username = fields.StringField(max_length=64, unique=True)
    password_hash = fields.StringField(max_length=200)
    email = fields.StringField(max_length=64, unique=True, index=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_json(self):
        return {"id": self.id, "username": self.username}


class Record(db.Document):
    user = fields.ReferenceField(users)
    player = fields.StringField(max_length=64, nullable=False)
    rank = fields.IntField(nullable=False)
    point = fields.IntField(nullable=False)
    survival = fields.IntField(nullable=False)
    insert_time = fields.DecimalField(nullable=False, default=time.time)
    insert_user = fields.ReferenceField(users)
    update_time = fields.DecimalField(
        nullable=False, onupdate=time.time, default=time.time
    )
    update_user = fields.ReferenceField(users)

###########
# reference:https://github.com/testdrivenio/flask-spa-auth/blob/master/flask-spa-same-origin/backend/app.py
#           https://github.com/PrettyPrinted/building_user_login_system/blob/master/finish/app.py
#           https://github.com/miguelgrinberg/flasky/blob/master/app/models.py
#           https://hackmd.io/@shaoeChen/HJiZtEngG/https%3A%2F%2Fhackmd.io%2Fs%2Fryvr_ly8f
#
###########
from flask import request
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt,
    get_jwt_identity,
    jwt_required,
)
from flask_restx import Resource
from mongoengine.queryset.visitor import Q

from main import jwt
from main.model import return_format, users

from . import AuthInit

auth = AuthInit.auth
blacklist = set()


@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
    jti = jwt_payload["jti"]
    return jti in blacklist


@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return return_format(401, False, data={{"data": "token expired"}})


@auth.route("/refresh")
class Refresh(Resource):
    RefreshSer = AuthInit.Refresh

    @jwt_required(refresh=True)
    def get(self):
        """更換access token"""
        try:
            current_user = get_jwt_identity()
            # 驗證失敗 回傳失敗
            if not current_user:
                raise Exception("token error")

            return return_format(
                data={"access_token": create_access_token(identity=current_user)}
            )
        except Exception as e:
            return return_format(400, False, data={{"errorResult": str(e)}})


@auth.route("/signup")
class Signup(Resource):
    SignupSer = AuthInit.Signup

    @auth.expect(SignupSer)
    def post(self):
        """註冊"""
        data = request.get_json()

        user = users.objects(
            Q(username=data["username"]) | Q(email=data["email"])
        ).first()
        print(user)

        if not user:
            new_user = users(
                username=data["username"],
                email=data["email"],
            )
            new_user.set_password(data["password"])
            new_user.save()
            return return_format()
        return return_format(
            400, False, data={"messages": "user or email has been used"}
        )


@auth.route("/login")
class Login(Resource):
    LoginSer = AuthInit.Login

    @auth.expect(LoginSer)
    def post(self):
        """登入"""
        data = request.get_json()
        user = data["user"]
        password = data["password"]

        user = users.objects(Q(username=user) | Q(email=user)).first()
        if user:
            if user.check_password(password):
                refresh_token = create_refresh_token(identity=user.email)
                access_token = create_access_token(identity=user.email)
                return return_format(
                    data={"refresh_token": refresh_token, "access_token": access_token}
                )
        return return_format(400, False, data={"messages": "user not found"})


@auth.route("/logout")
class Logout(Resource):
    @jwt_required(verify_type=False)
    def delete(self):
        """登出"""
        token = get_jwt()
        jti = token["jti"]
        ttype = token["type"]
        blacklist.add(jti)
        return return_format(
            data={"data": f"{ttype.capitalize()} token successfully revoked"}
        )

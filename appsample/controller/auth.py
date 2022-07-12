###########
# reference:https://github.com/testdrivenio/flask-spa-auth/blob/master/flask-spa-same-origin/backend/app.py
#           https://github.com/PrettyPrinted/building_user_login_system/blob/master/finish/app.py
#           https://github.com/miguelgrinberg/flasky/blob/master/app/models.py
#           https://hackmd.io/@shaoeChen/HJiZtEngG/https%3A%2F%2Fhackmd.io%2Fs%2Fryvr_ly8f
#
###########
from .. import jwt
from ..model import User, db, return_format
from flask import Blueprint, request
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt
auth = Blueprint('auth', __name__)
blacklist = set()


@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
    jti = jwt_payload["jti"]
    return jti in blacklist


@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return return_format(401, False, data={{"data": "token expired"}})


@auth.route('/refresh', methods=['GET'])
@jwt_required(refresh=True)
def refresh():
    """
    更換access token
    ---
    tags:
      - auth
    produces: application/json
    security:
      - BearerAuth: ['Authorization']
    responses:
      404:
        description: Page Not Fond
      500:
        description: Internal Server Error
      200:
        description: OK
    """
    try:
        current_user = get_jwt_identity()
        # 驗證失敗 回傳失敗
        if not current_user:
            raise Exception('token error')

        return return_format(data={"access_token": create_access_token(identity=current_user)})
    except Exception as e:
        return return_format(400, False, data={{"errorResult": str(e)}})


@auth.route('/signup', methods=['POST'])
def signup():
    """
    註冊
    ---
    tags:
      - auth
    parameters:
      - name: body
        in: body
        required: true
        schema:
          required:
            - email
            - username
            - password
          properties:
            username:
              type: string
            password:
              type: string
            email:
              type: string
    produces: application/json
    responses:
      404:
        description: Page Not Fond
      500:
        description: Internal Server Error
      200:
        description: OK
    """
    data = request.get_json()
    user = data['username']
    email = data['email']

    user = User.query.filter((User.username == user) | (User.email == email)).first()

    if not user:
        new_user = User(**data)
        db.session.add(new_user)
        db.session.commit()
        return return_format()
    return return_format(400, False, data={"messages": "user or email has been used"})


@auth.route("/login", methods=["POST"])
def login():
    """
    登入
    ---
    tags:
      - auth
    parameters:
      - name: body
        in: body
        required: true
        schema:
          required:
            - user
            - password
          properties:
            user:
              type: string
            password:
              type: string
    produces: application/json
    responses:
      404:
        description: Page Not Fond
      500:
        description: Internal Server Error
      200:
        description: OK
    """
    data = request.get_json()
    user = data['user']
    password = data['password']

    user = User.query.filter((User.username == user) | (User.email == user)).first()
    if user:
        if user.check_password(password):
            refresh_token = create_refresh_token(identity=user.id)
            access_token = create_access_token(identity=user.id)
            return return_format(data={"refresh_token": refresh_token, "access_token": access_token})

    return return_format(400, False, data={"messages": "user not found"})


@auth.route("/logout", methods=["DELETE"])
@jwt_required(verify_type=False)
def logout():
    """
    登出
    ---
    tags:
      - auth
    produces: application/json
    security:
      - BearerAuth: ['Authorization']
    responses:
      404:
        description: Page Not Fond
      500:
        description: Internal Server Error
      200:
        description: OK
    """
    token = get_jwt()
    jti = token["jti"]
    ttype = token["type"]
    blacklist.add(jti)
    return return_format(data={"data": f"{ttype.capitalize()} token successfully revoked"})

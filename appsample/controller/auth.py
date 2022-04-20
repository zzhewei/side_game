###########
# reference:https://github.com/testdrivenio/flask-spa-auth/blob/master/flask-spa-same-origin/backend/app.py
#           https://github.com/PrettyPrinted/building_user_login_system/blob/master/finish/app.py
#           https://github.com/miguelgrinberg/flasky/blob/master/app/models.py
#           https://hackmd.io/@shaoeChen/HJiZtEngG/https%3A%2F%2Fhackmd.io%2Fs%2Fryvr_ly8f
###########
from flask_login import login_required, login_user, logout_user
from .. import login_manager, csrf
from ..model import User, db
from flask import Blueprint, request, jsonify
from flask_wtf.csrf import generate_csrf
auth = Blueprint('auth', __name__)


@login_manager.user_loader
def load_user(uid):
    return User.query.get(uid)


@auth.route("/GetCsrf", methods=["GET"])
@csrf.exempt
def get_csrf():
    """
    取得token
    ---
    tags:
      - token
    produces: application/json
    responses:
      404:
        description: Page Not Fond
      500:
        description: Internal Server Error
      200:
        description: OK
    """
    token = generate_csrf()
    response = jsonify({"Success": True, "X-CSRFToken": token})
    print("Get token remove IP: ", request.remote_addr)
    print(token)
    response.headers.set("X-CSRFToken", token)
    return response


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
            - username
            - password
          properties:
            username:
              type: string
            password:
              type: string
    security:
      - APIKeyHeader: ['X-CSRFToken']
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

    new_user = User(**data)
    db.session.add(new_user)
    db.session.commit()
    data = {"code": 200, "success": True, "data": "success"}
    return jsonify(data)


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
            - username
            - password
          properties:
            username:
              type: string
            password:
              type: string
    security:
      - APIKeyHeader: ['X-CSRFToken']
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
    username = data['username']
    password = data['password']

    user = User.query.filter_by(username=username).first()
    if user:
        if user.check_password(password):
            login_user(user)
            response = jsonify({"login": True})
            return response

    return jsonify({"login": False})


@auth.route("/logout")
@login_required
def logout():
    """
    登出
    ---
    tags:
      - auth
    produces: application/json
    responses:
      404:
        description: Page Not Fond
      500:
        description: Internal Server Error
      200:
        description: OK
    """
    logout_user()
    return jsonify({"logout": True})

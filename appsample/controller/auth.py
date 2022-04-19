###########
# reference:https://github.com/testdrivenio/flask-spa-auth/blob/master/flask-spa-same-origin/backend/app.py
#           https://github.com/PrettyPrinted/building_user_login_system/blob/master/finish/app.py
#           https://github.com/miguelgrinberg/flasky/blob/master/app/models.py
#           https://hackmd.io/@shaoeChen/HJiZtEngG/https%3A%2F%2Fhackmd.io%2Fs%2Fryvr_ly8f
###########
from flask_login import login_required, login_user, logout_user, current_user
from .. import login_manager, csrf
from ..model import User, db
from flask import Blueprint, request, jsonify
from flask_wtf.csrf import generate_csrf
auth = Blueprint('auth', __name__)


@login_manager.user_loader
def load_user(uid):
    return User.query.get(uid)


@auth.route("/GetCsrf", methods=["GET"])
def get_csrf():
    token = generate_csrf()
    response = jsonify({"Success": True})
    response.headers.set("csrf_token", token)
    return response


@auth.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data['username']
    password = data['password']

    new_user = User(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()
    data = {"code": 200, "success": "true", "data": "success"}
    return jsonify(data)


@auth.route("/login", methods=["POST"])
# @csrf.exempt
def login():
    """
    登入
    ---
    tags:
      - test
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
      - test
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


@auth.route('/session', methods=["POST"])
def get_session():
    if not current_user.is_authenticated:
        return jsonify({'status': 'error'}), 401
    return jsonify({'status': 'success', 'user': current_user.to_json()})

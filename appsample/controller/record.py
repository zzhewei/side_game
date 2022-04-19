import json
from flask_login import login_required
from ..model import select, sqlOP, Permission, Record, db
from flask import Blueprint, jsonify, current_app, request
from ..decorators import permission_required
from datetime import datetime
from .. import csrf
record = Blueprint('record', __name__)


# insert record
@record.route("/Insert_Record", methods=['POST'])
@login_required
def Insert_Record():
    """
    新增紀錄
    ---
    tags:
      - Record
    parameters:
      - name: body
        in: body
        required: true
        schema:
          required:
            - uid
            - rank
            - point
          properties:
            uid:
              type: integer
            rank:
              type: integer
            point:
              type: integer
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
    try:
        data = request.get_json()
        userid = data['uid']
        rank = data['rank']
        point = data['point']
        current_app.logger.warning("Insert Record...")
        new_user = Record(uid=userid, rank=rank, point=point, insert_time=datetime.now(), insert_user=userid, update_time=datetime.now(), update_user=userid)
        db.session.add(new_user)
        db.session.commit()
        current_app.logger.warning("Insert Complete!")

        data = {"code": 200, "success": True, "data": "success"}
    except Exception as e:
        result = [{"errorResult": str(e)}]
        data = {"code": 400, "success": "false", "data": result}
        current_app.logger.error("Error:", e)
    return jsonify(data)


# query record
@record.route("/QueryRecord", methods=['POST'])
@csrf.exempt
def QueryRecord():
    """
    查詢紀錄
    ---
    tags:
      - Record
    produces: application/json
    parameters:
      - name: body
        in: body
        required: true
        schema:
          required:
            - uid
          properties:
            uid:
              type: integer
    responses:
      404:
        description: Page Not Fond
      500:
        description: Internal Server Error
      200:
        description: OK
    """
    try:
        data = request.get_json()
        userid = data['uid']
        current_app.logger.warning("simple page info...")

        return_data = select("SELECT username, Record.rank, point, insert_time FROM Record left join user on Record.uid = user.id;")
        for i, item in enumerate(return_data):
            return_data[i] = dict(item)
        data = {"code": 200, "success": True, "data": return_data}
    except Exception as e:
        result = [{"errorResult": str(e)}]
        data = {"code": 400, "success": False, "data": result}
    return jsonify(data)

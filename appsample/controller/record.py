import json
from flask_login import login_required, current_user
from ..model import select, sqlOP, Permission, Record, db, return_format
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
        rank = data['rank']
        point = data['point']
        current_app.logger.warning("Insert Record...")
        new_user = Record(uid=current_user.get_id(), rank=rank, point=point, insert_time=datetime.now(), insert_user=current_user.get_id(), update_time=datetime.now(), update_user=current_user.get_id())
        db.session.add(new_user)
        db.session.commit()
        current_app.logger.warning("Insert Complete!")

        return return_format()
    except Exception as e:
        current_app.logger.error("Error:", e)
        return return_format(400, False, data={"messages": str(e)})


# query record
@record.route("/QueryRecord", methods=['POST'])
@csrf.exempt
def QueryRecord():
    """
    查詢紀錄
    全部帶0 or ""
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
        uid = data['uid']
        current_app.logger.warning("simple page info...")
        if uid:
            return_data = select("SELECT username, Record.rank, point, insert_time FROM Record left join public.user on Record.uid = public.user.id where uid=:uid order by point desc, rank desc;", {'uid': uid})
        else:
            return_data = select("SELECT username, Record.rank, point, insert_time FROM Record left join public.user on Record.uid = public.user.id order by point desc, rank desc;")
        for i, item in enumerate(return_data):
            return_data[i] = dict(item)
        return return_format(data={"data": return_data})
    except Exception as e:
        current_app.logger.error("Error:", e)
        return return_format(400, False, data={"messages": str(e)})

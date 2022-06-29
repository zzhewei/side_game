from ..model import Record, db, return_format, User
from flask import Blueprint, current_app, request
from ..decorators import permission_required
from flask_jwt_extended import jwt_required, get_jwt_identity
record = Blueprint('record', __name__)


# insert record
@record.route("/Insert_Record", methods=['POST'])
@jwt_required(optional=True)
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
            - username
            - rank
            - point
            - survival
          properties:
            username:
              type: string
            rank:
              type: integer
            point:
              type: integer
            survival:
              type: integer
    security:
      - BearerAuth: ['Authorization']
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
        username = data['username']
        rank = data['rank']
        point = data['point']
        survival = data['survival']
        current_app.logger.warning("Insert Record...")

        current_user = get_jwt_identity()
        print(current_user)
        if current_user:
            new_record = Record(uid=current_user, player="", rank=rank, point=point, survival=survival, insert_user=current_user, update_user=current_user)
        elif username:
            new_record = Record(player=username, rank=rank, point=point, survival=survival, insert_user=username, update_user=username)
        else:
            return return_format(401, False, data={"messages": "token expired or username is null"})
        db.session.add(new_record)
        db.session.commit()
        current_app.logger.warning("Insert Complete!")

        return return_format()
    except Exception as e:
        current_app.logger.error("Error:", e)
        return return_format(400, False, data={"messages": str(e)})


# query record
@record.route("/QueryRecord/<int:page>/<int:count>", methods=['POST'])
@jwt_required(optional=True)
def QueryRecord(page=1, count=10):
    """
    查詢紀錄
    看全部帶false

    page是頁數
    count是一頁幾個
    ---
    tags:
      - Record
    produces: application/json
    parameters:
      - name: page
        in: path
        required: true
        default: 1
      - name: count
        in: path
        required: true
        default: 5
      - name: body
        in: body
        required: true
        schema:
          required:
            - self
          properties:
            self:
              type: boolean
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
        data = request.get_json()
        self = data['self']
        print(self)
        current_user = get_jwt_identity()

        # 有登入並要看自己紀錄
        if self and current_user:
            return_data = Record.query.filter_by(uid=current_user).with_entities(User.username, Record.player, Record.rank, Record.point, Record.survival, Record.insert_time).join(User, User.id == Record.uid, isouter=True)\
                .order_by(Record.rank.desc(), Record.point.desc(), Record.survival.asc()).paginate(page, count, False)

        # 有登入要看全部及遊客
        else:
            return_data = Record.query.with_entities(User.username, Record.player, Record.rank, Record.point, Record.survival, Record.insert_time).join(User, Record.uid == User.id, isouter=True)\
                .order_by(Record.rank.desc(), Record.point.desc(), Record.survival.asc()).paginate(page, count, False)

        result = []
        for i in return_data.items:
            temp = {"rank": i.rank, "point": i.point, "survival": i.survival, "insert_time": i.insert_time}
            # 遊客沒有uid 所以要比對確認
            if i.username:
                temp["username"] = i.username
            else:
                temp["username"] = i.player
            result.append(temp)
        return return_format(data={"data": result})
    except Exception as e:
        current_app.logger.error("Error:", e)
        return return_format(400, False, data={"messages": str(e)})

from flask import current_app, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restx import Resource

from main.model import Record, return_format, users

from . import RecordInit

record = RecordInit.record


@record.route("/Insert_Record")
class InsertRecord(Resource):
    InsertSer = RecordInit.Insert

    @record.expect(InsertSer)
    @jwt_required(optional=True)
    def post(self):
        """新增紀錄"""
        data = request.get_json()
        username = data["username"]
        rank = data["rank"]
        point = data["point"]
        survival = data["survival"]
        current_app.logger.info("Insert Record...")

        current_user = get_jwt_identity()
        print(current_user)
        if current_user:
            u = users.objects.get(email=current_user)
            new_record = Record(
                user=u,
                player="",
                rank=rank,
                point=point,
                survival=survival,
                insert_user=u,
                update_user=u,
            )
        elif username:
            new_record = Record(
                player=username,
                rank=rank,
                point=point,
                survival=survival,
                insert_user=username,
                update_user=username,
            )
        else:
            return return_format(
                401, False, data={"messages": "token expired or username is null"}
            )
        new_record.save()
        current_app.logger.info("Insert Complete!")

        return return_format()


@record.route("/QueryRecord/<int:page>/<int:count>")
class QueryRecord(Resource):
    QuerySer = RecordInit.Query
    QueryRSer = RecordInit.QueryR

    @record.expect(QuerySer)
    @jwt_required(optional=True)
    def post(self, page=1, count=10):
        """查詢紀錄
        看全部帶false

        page是頁數
        count是一頁幾個"""
        data = request.get_json()
        sel = data["self"]
        current_user = get_jwt_identity()
        select_data = []

        # 有登入並要看自己紀錄
        if sel and current_user:
            user = users.objects.get(email=current_user)
            select_data = [{"$match": {"user": user.id}}]
        # 有登入要看全部或遊客
        else:
            pass

        select_data += [
            {
                "$lookup": {
                    "from": "users",  # 要聯合的集合名稱
                    "localField": "user",
                    "foreignField": "_id",
                    "as": "user_data",
                }
            },
            {
                "$project": {
                    "player": 1,
                    "rank": 1,
                    "point": 1,
                    "survival": 1,
                    "insert_time": 1,
                    "user_data.username": 1,  # 要顯示那些欄位
                }
            },
            {
                "$sort": {"rank": -1, "point": -1, "survival": 1},  # -1 = desc, 1 = asc
            },
            {"$skip": (page - 1) * count},  # 跳過幾個
            {"$limit": count},  # 一頁幾個
        ]

        return_data = Record.objects.aggregate(select_data)
        result = []
        for i in return_data:
            temp = {
                "rank": i["rank"],
                "point": i["point"],
                "survival": i["survival"],
                "insert_time": i["insert_time"],
            }
            # 遊客沒有uid 所以要比對確認
            if i["user_data"]:
                temp["username"] = i["user_data"][0]["username"]
            else:
                temp["username"] = i["player"]
            result.append(temp)
        return return_format(data=result)

from flask_restx import Namespace, fields


class RecordInit:
    record = Namespace("Record", path="/", description="Record")

    Insert = record.model(
        "Insert",
        {
            "point": fields.Integer,
            "rank": fields.Integer,
            "survival": fields.Integer,
            "username": fields.String,
        },
    )

    Query = record.model(
        "Query",
        {
            "self": fields.Boolean,
        },
    )

    QueryR = record.model(
        "QueryR",
        {
            "point": fields.Integer,
            "rank": fields.Integer,
            "survival": fields.Integer,
            "username": fields.String,
            "insert_time": fields.String,
        },
    )

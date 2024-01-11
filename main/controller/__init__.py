from flask import Blueprint
from flask_restx import Api

from .auth.views import auth
from .record.views import record

v1 = Blueprint("v1", __name__, url_prefix="/API")
api = Api(
    v1,
    version="1.0",
    title="SideGame API",
    description="Just API",
    security="Bearer Auth",
    authorizations={
        "Bearer Auth": {
            "type": "apiKey",
            "in": "header",
            "name": "Authorization",
            "description": "Add a jwt with ** Bearer token",
        }
    },
)

api.add_namespace(record)
api.add_namespace(auth)

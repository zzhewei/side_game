from flask_restx import Namespace, fields


class AuthInit:
    auth = Namespace("Auth", path="/", description="Auth")

    Refresh = auth.model(
        "Refresh",
        {
            "access_token": fields.String,
        },
    )

    Signup = auth.model(
        "Signup",
        {
            "email": fields.String,
            "username": fields.String,
            "password": fields.String,
        },
    )

    Login = auth.model(
        "Login",
        {
            "user": fields.String,
            "password": fields.String,
        },
    )

    RemainDELETE = auth.model(
        "RemainDELETE",
        {"RemainIdList": fields.List(fields.Integer)},
    )

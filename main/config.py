import os
from datetime import timedelta


class BaseConfig:  # 基本配置
    SECRET_KEY = os.urandom(24)
    # 不設定的話Flask會使用緩存的js跟css不會更新
    SEND_FILE_MAX_AGE_DEFAULT = timedelta(seconds=1)
    # 中文設置
    JSON_AS_ASCII = False
    # SWAGGER設置  /apidocs
    SWAGGER = {
        "title": "Game API",
        "description": "",
        "version": "1.0.0",
        "termsOfService": "",
        "hide_top_bar": True,
    }
    # 設定 JWT 密鑰
    JWT_SECRET_KEY = "side_game_is_good"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=1)


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    WTF_CSRF_CHECK_DEFAULT = True
    WTF_CSRF_SSL_STRICT = True
    MONGODB_DB = "test"
    MONGODB_HOST = "localhost"
    MONGODB_PORT = 27017
    MONGODB_USERNAME = "root"
    MONGODB_PASSWORD = "root"


class TestingConfig(BaseConfig):
    TESTING = True


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
}

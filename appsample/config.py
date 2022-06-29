from datetime import timedelta
import os


class BaseConfig:  #基本配置
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
        "hide_top_bar": True
    }
    # 設定 JWT 密鑰
    JWT_SECRET_KEY = 'side_game_is_good'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=1)


class DevelopmentConfig(BaseConfig):
    DEBUG = False
    WTF_CSRF_CHECK_DEFAULT = True
    WTF_CSRF_SSL_STRICT = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:root@localhost:3306/game"
    # SQLALCHEMY_DATABASE_URI = "postgresql://postgres:root@localhost:5432/game"
    SQLALCHEMY_DATABASE_URI = "postgresql://iedwpgwuvcgsoo:7c20b1aa2e70f510c83493bdfe07311c314e420e151b34225aabdc6c1cfad605@ec2-34-194-158-176.compute-1.amazonaws.com:5432/d6rfpl9vn6ib7m"
    # if use docker compose use this
    # SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:root@mysql:3306/game"


class TestingConfig(BaseConfig):
    TESTING = True


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
}

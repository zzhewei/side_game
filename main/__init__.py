import logging
from logging.handlers import TimedRotatingFileHandler

from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from werkzeug.utils import import_string

from .config import config
from .model import db

jwt = JWTManager()


##########
# 工廠模式
# 初始化 Flask對象可以是package或檔案 __name__是系統變數，該變數指的是該py檔的名稱
##########
def create_app(config_name, blueprints):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    for i in blueprints:
        import_name = import_string(i)
        app.register_blueprint(import_name)
    CORS(app)
    db.init_app(app)
    jwt.init_app(app)

    formatter = logging.Formatter(
        "%(asctime)s [%(filename)s:%(lineno)d][%(levelname)s] - %(message)s"
    )
    handler = TimedRotatingFileHandler(
        "./log/event.log",
        when="D",
        interval=1,
        backupCount=15,
        encoding="UTF-8",
        delay=True,
        utc=True,
    )
    app.logger.addHandler(handler)
    handler.setFormatter(formatter)

    return app

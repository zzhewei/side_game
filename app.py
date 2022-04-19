from gevent import monkey
monkey.patch_all()  # 異步 基於greenlet
from gevent import pywsgi
from appsample import create_app


# if need test change controller to test
blueprints = ['appsample.controller.user:test',
              'appsample.controller.auth:auth']
# if need test change development to testing
app = create_app('development', blueprints)


if __name__ == '__main__':
    server = pywsgi.WSGIServer(('0.0.0.0', 9898), app)  # 需使用支持 gevent 的 WSGI
    server.serve_forever()

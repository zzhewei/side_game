#from gevent import monkey
#monkey.patch_all()  # 異步 基於greenlet
from gevent import pywsgi
from appsample import create_app


# if need test change controller to test
blueprints = ['appsample.controller.record:record',
              'appsample.controller.auth:auth']
# if need test change development to testing
app = create_app('development', blueprints)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="9998")
    #server = pywsgi.WSGIServer(('0.0.0.0', 9998), app)  # 需使用支持 gevent 的 WSGI
    #server.serve_forever()

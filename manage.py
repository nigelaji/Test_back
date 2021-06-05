# coding:utf-8
from tp_app import app

# from ws_app import sockets_app
# from gevent import pywsgi
# from geventwebsocket.handler import WebSocketHandler

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)

    # server = pywsgi.WSGIServer(('0.0.0.0', 8540), application=sockets_app, handler_class=WebSocketHandler)
    # print('server started : 0.0.0.0:8540')
    # server.serve_forever()

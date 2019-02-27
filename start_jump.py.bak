from gevent import monkey
#这个猴子补丁可以让 同步阻塞，变成异步非阻塞
monkey.patch_all()

import argparse
import os
#用gevent的wsgi 代替原有的django的 wsgi
from  gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler
#导入django的应用,让gevent成为django的 wsgi
from ironfort.wsgi import application

version = '1.0.0'

#获取当前目录
root_path = os.path.dirname(__file__)

#抓跟参
parser = argparse.ArgumentParser(description='Jumpserver，基于django与websocket')
parser.add_argument('--port', '-p',
                    type=int,
                    default=8000,
                    help='服务器端口，默认为8000')

parser.add_argument('--host', '-H',
                    default='0.0.0.0',
                    help='服务器IP，默认为0.0.0.0')

args = parser.parse_args()

print('\033[31mJumpserver\033[0m {0}  running on  {1} : {2}'.format(version, args.host, args.port))

#创建gevent服务器
ws_server = WSGIServer(
    (args.host, args.port),
    application,
    #log=None
    handler_class=WebSocketHandler
)

try:
    ws_server.serve_forever()
except KeyboardInterrupt:
    print('服务器关闭......')
    pass
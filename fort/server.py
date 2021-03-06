import gevent
from gevent.socket import wait_read, wait_write
import paramiko
import json
from . import models


def add_log(user, content, log_type='1'):
    try:
        models.AccessLog.objects.create(
            user=user,
            log_type=log_type,
            content=content
        )
    except Exception as e:
        print('保存日志的过程中发生了错误：', e)




class WSSHBridge(object):
    """
    桥接websocket和SSH的核心类
    """

    def __init__(self, websocket, user):
        self.user = user
        self._websocket = websocket
        self._tasks = []
        self.trans = None
        self.channel = None
        self.cmd_string = ''

    def open(self, host_ip, port=22, username=None, password=None):
        """
        建立SSH连接
        :param host_ip:
        :param port:
        :param username:
        :param password:
        :return:
        """
        try:
            self.trans = paramiko.Transport((host_ip, port))
            self.trans.start_client()
            self.trans.auth_password(username=username, password=password)
            channel = self.trans.open_session()
            channel.get_pty()
            self.channel = channel
        except Exception as e:
            self._websocket.send(json.dumps({'error': e}))
            raise

    def _forward_inbound(self, channel):
        """
        正向数据转发，websocket ->  ssh
        :param channel:
        :return:
        """
        try:
            while True:
                data = self._websocket.receive()
                if not data:
                    return
                data = json.loads(str(data))

                if 'data' in data:
                    # print('websocket -> ssh', data['data'])
                    self.cmd_string += data['data']
                    channel.send(data['data'])
        finally:
            self.close()

    def _forward_outbound(self, channel):
        """
        反向数据转发，ssh -> websocket
        :param channel:
        :return:
        """
        try:
            while True:
                wait_read(channel.fileno())
                data = channel.recv(1024)
                if not len(data):
                    return
                self._websocket.send(json.dumps({'data': data.decode()}))
        finally:
            self.close()

    def _bridge(self, channel):
        """
        全双工通信
        :param channel:
        :return:
        """
        #关闭同步阻塞
        channel.setblocking(False)
        #设置延时
        channel.settimeout(0.0)
        self._tasks = [
            gevent.spawn(self._forward_inbound, channel),
            gevent.spawn(self._forward_outbound, channel),
        ]
        gevent.joinall(self._tasks)

    def close(self):
        """
        结束桥接会话
        :return:
        """
        gevent.killall(self._tasks, block=True)
        #清空gevent
        self._tasks = []

    def shell(self):
        """
        启动一个shell通信界面
        :return:
        """
        self.channel.invoke_shell()
        self._bridge(self.channel)
        self.channel.close()
        # 创建日志
        add_log(self.user, self.cmd_string)

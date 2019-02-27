from django.contrib.auth import authenticate
from fort import models
import os
from django.db.models import Q
from . import paramiko_ssh


class SshHandler(object):
    """堡垒机交互脚本"""
    def __init__(self, argv_handler_instance):
        self.argv_handler_instance = argv_handler_instance
        self.models = models

    def auth(self):
        '''认证程序'''
        count = 0
        while count < 3:
            username = input('堡垒机账户：').strip()
            password = input('堡垒机密码：').strip()

            user = authenticate(username=username, password=password)

            if user:
                self.user = user
                return True
            else:
                count += 1

    def interactive(self):
        if self.auth():
            while True:
                _host = []
                remote_user_bind_host = models.RemoteUserBindHost.objects.filter(
                    Q(enabled=True),
                    Q(userprofile__user=self.user) | Q(group__userprofile__user=self.user)
                ).distinct()
                print('\033[32m Welcome  \033[0m \n',
                      '\033[32m 1) 输入 p 打印主机列表 \033[0m \n',
                      '\033[32m 2) 输入完整 IP 进行登录 \033[0m \n',
                      '\033[32m 3) 输入 b 返回主菜单 \033[0m \n',
                      '\033[32m 4) 输入 q 退出 \033[0m \n')
                choice = input('ops >>').strip()
                if choice == 'p':
                    while True:
                        for index, host_to_user_obj in enumerate(remote_user_bind_host):
                            print(" %s \t %s" % (host_to_user_obj.host.ip,host_to_user_obj.host.hostname))
                            _host.append(host_to_user_obj.host.ip)
                        choice = input('选择主机 >>').strip()
                        if choice in _host:
                            choice = _host.index(choice)
                        # 判断字符串是不是 由数字组成
                        #if choice.isdigit():
                            choice = int(choice)
                            # 获取选择对应下标的组信息
                            hosts = remote_user_bind_host[choice]
                            paramiko_ssh.ssh_connect(self, hosts)
                        elif choice == 'b':
                            break
                        else:
                            continue
                elif choice == 'q':
                    exit()
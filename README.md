# Lj平台
[![python3.x](https://img.shields.io/badge/python-3.4.8-blue.svg)](https://www.python.org/)
[![django](https://img.shields.io/badge/django-2.0.8-blue.svg)](https://www.djangoproject.com/)
[![websocket](https://img.shields.io/badge/websocket-green.svg)](https://github.com/search?q=websocket)


## 平台介绍
由于写的过于垃圾，于是起名垃圾平台，为个人练手项目  
###远程连接方面：  
1.目前支持web 终端(贼难用)  
2.backend为linux端脚本，使用方法，取跳板机一普通用户，用作ssh连接，再用户家目录下的.bashrc(记不准了)，写入执行脚本的命令，做到ssh登录后自动运行脚本，脚本会让用户手动输入平台账号密码，脚本会循环print当前用户可用主机，输入ip才能远程过去。  
3.有个日志功能(不是录屏),能记录使用过的基本命令，目前仅admin用户可看。  
4.上传和下载文件，上传支持多ip同时上传同一文件，下载仅支持单ip下载(谁让我low啊)
###次产统计方面：  
还没写呢  

## 项目部署
### 1. 克隆项目
``` bash
git clone https://github.com/vitaureatea/ironfort.git
```
### 2. 环境依赖
```
#mysql5.7 or sqlit
#Linux
```
### 3. 配置项目
```
# 安装python依赖
cd ironfort
pip install -r requirements.txt

# 配置数据库
settings.py 
本项目使用mysql数据库，pymysql模块

# 生成数据库文件
python manage.py makemigrations 

#初始化数据库
python manage.py migrate

#创建admin用户
python manage.py createsuperuser 

#启动
#默认为0.0.0.0：8000
cd ironfort
python manage.py runserver
```


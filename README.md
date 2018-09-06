# Jumpserver
[![python3.x](https://img.shields.io/badge/python-3.4.8-blue.svg)](https://www.python.org/)
[![django](https://img.shields.io/badge/django-2.0.8-blue.svg)](https://www.djangoproject.com/)
[![websocket](https://img.shields.io/badge/websocket-green.svg)](https://github.com/search?q=websocket)


跳板机目前只有操作记录查询功能，和webssh功能，以及很low的命令行shell

## 项目部署
### 1. 克隆项目
``` bash
git clone https://github.com/vitaureatea/ironfort.git
```
### 2. 环境依赖
```
#mysql
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
python start_jump.py  
```
### 4. 未来打算
```
1，批量执行命令
2，批量分发文件
```

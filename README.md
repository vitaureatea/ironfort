# Lj平台
[![python3.x](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/)
[![django](https://img.shields.io/badge/django-2.0.8-blue.svg)](https://www.djangoproject.com/)


## 平台功能简介
由于写的过于垃圾，于是起名垃圾平台，采用乱七八糟写法，后台为Django自带后台。
### 堡垒机：  
1.支持web 终端(贼难用)  
2.支持linux命令行终端，backend为linux端脚本，使用方法，取跳板机一普通用户，用作ssh连接，在用户家目录下的.bashrc(记不准了)，写入执行脚本的命令，做到ssh登录后自动运行脚本，脚本会让用户手动输入平台账号密码，脚本会循环print当前用户可用主机，输入ip才能远程过去。  
3.日志记录：可记录使用过的基本命令，目前仅admin用户可看。  
### 文件传输：
1.上传和下载文件，上传支持多ip同时上传同一文件，下载仅支持单ip下载(谁让我low啊)
### 资产统计：  
还没写呢  

## 项目使用
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
或者自带的 SQLIT 随便

# 生成数据库文件
python manage.py makemigrations 

#初始化数据库
python manage.py migrate

#创建admin用户
python manage.py createsuperuser 

#启动
#默认为 0.0.0.0:8000
cd ironfort
python start_jump.py
```
### 4.linux端的backend
```
useradd newuser  
vim newuser/.bashrc  加入：  

python3 PATH/ironfort/bk_manage.py run
logout  

通过登录newuser 即可触发脚本 
```
### 未来打算
```
如果未来，学会了前端，以及后端，可能会鼓起勇气重写
```

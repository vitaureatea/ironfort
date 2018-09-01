from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth import authenticate
#此为django的auth认证
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from . import models
import random,os
from PIL import Image
from .server import WSSHBridge,add_log



def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)
        # 如果方法执行失败，返货的对象为null
        request.session['username'] = username
        if user is not  None:
            userprofile = models.UserProfile.objects.get(user=user)
            print(userprofile)
            if userprofile.enabled:
                #如果账号已启用
                auth_login(request,user)
                #采用django自带longin
                return redirect('/index/')
            else:
                message = '账号未启用，请联系管理员'
                return render(request, 'login.html', {"message": message})
        else:
            message = '登陆失败，账号或密码错误'
            return render(request, 'login.html', {'message': message})
    if request.method == 'GET':
        if request.session.get('username') is not None:
            return redirect('/index/')
        else:
            return render(request, 'login.html', locals())



@login_required(login_url='/login/')
def logout(request):
    auth_logout(request)
    #django自带退出
    return redirect('/login/')



@login_required(login_url='/login/')  #进制未登录直接访问首页
#因为使用的django自带的登录，也可以用django自带的装饰器判断用户是否登录，如果未登录，就跳转到url
def index (request):
    #知道当前登录用户的主机信息
    remote_user_bind_host = models.RemoteUserBindHost.objects.filter(
        Q(enabled = True),
        Q(userprofile__user = request.user) | Q(group__userprofile__user = request.user)
    ).distinct()
    #联合查询，Q 都好表示和and | 表示或   enable为必须条件，下面俩有一个就行了
    #账号本身能访问的 主机，以及账户所属组能访问的主机
    #.distinct() 去重
    pro = models.UserInfo.objects.filter(user=request.user)
    return render(request,'index.html',{'remote_user_bind_host': remote_user_bind_host,'pro': pro},)




@login_required(login_url='/login/')  #进制未登录直接访问首页
def profile(request):
    pro = models.UserInfo.objects.filter(user = request.user)
    return render(request,'profile.html',{'pro': pro})



@login_required(login_url='/login/')
def update_head(request):
    if request.method == 'POST':
        if request.FILES.get('image'):
            #user = getattr(request, 'user', None)
            info = models.UserInfo.objects.get(user = request.user)
            # 在更新头像之前 先删除掉以前的头像
            # 担心误操作已经删除过头像所以这这里try一下
            try:
                os.remove('./static/' + str(info.image))
            except:
                pass

            # 获取上传的文件对象
            image = request.FILES.get('image')
            print(image)
            filename = ''.join([random.choice('1324345656789ewretrytuyusfdgfh') for i in range(20)]) + os.path.splitext(image.name)[1]
            full_path = './static/dist/img/userhead/' + str(filename)
            with open(full_path, 'wb') as file:
                for chunk in image.chunks():
                    file.write(chunk)
            if info:
                # 保存数据库
                info.image = 'dist/img/userhead/' + str(filename)
                info.save()
                #做成缩略图
                img = Image.open(full_path)
                img.thumbnail((160,160))
                img.save(full_path)
        else:
            pass
    return redirect('/profile/')



@login_required(login_url='/login/')
def connect(request, user_bind_host_id):
    # 　如果当前请求不是websocket请求则退出
    if not request.environ.get('wsgi.websocket'):
        return HttpResponse('错误，非websocket请求！')
    try:
        remote_user_bind_host = models.RemoteUserBindHost.objects.filter(
            Q(enabled=True),
            Q(id=user_bind_host_id),
            Q(userprofile__user=request.user) | Q(group__userprofile__user=request.user)).distinct()[0]
            #和上面一样，账户是启用的而且 机器id是参数id ，账户也是有这个权限的，或者所属组有权限的
    except Exception as e:
        message = '无效的账户或者无权访问！\n' + str(e)
        add_log(request.user, message, log_type='3')
        return HttpResponse('请求主机发生错误')

    message = '来自{remote}的请求 尝试连接 -> {username} @ {hostname}  <{ip} : {port}>'.format(
        remote=request.META.get('REMOTE_ADDR'),
        username=remote_user_bind_host.remote_user.remote_user_name,
        hostname=remote_user_bind_host.host.hostname,
        ip=remote_user_bind_host.host.ip,
        port=remote_user_bind_host.host.port
    )
    add_log(request.user, message, log_type='2')
    print(message)

    #创建对象
    bridge = WSSHBridge(request.environ.get('wsgi.websocket'),request.user)

    #调用open方法
    try:
        bridge.open(
            host_ip=remote_user_bind_host.host.ip,
            port=remote_user_bind_host.host.port,
            username=remote_user_bind_host.remote_user.remote_user_name,
            password=remote_user_bind_host.remote_user.password
        )
    except Exception as e:
        message = '尝试连接{0}的过程中发生错误：\n {1}'.format(
            remote_user_bind_host.remote_user.remote_user_name, e)
        print(message)
        add_log(request.user, message, log_type='3')
        return HttpResponse("错误！无法建立SSH连接！")

    #最主要的数据通信就一行
    bridge.shell()

    #关闭websocket
    request.environ.get('wsgi.websocket').close()
    print('用户断开连接')
    return HttpResponse('200')


@login_required(login_url='/login/')
def get_log(request):
    #判断超级用户
    if request.user.is_superuser:
        logs = models.AccessLog.objects.all()
        pro = models.UserInfo.objects.filter(user=request.user)
        return render(request,'log.html',{'logs': logs,'pro': pro})
    else:
        add_log(request.user,'非超级用户尝试访问日志',logs_type='3')
        return redirect('/index/')

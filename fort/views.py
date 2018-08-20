from django.shortcuts import render,redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
#由于之前使用的django自带的User表，这里使用django自带的 auth方法
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from . import models


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)
        print(user)
        #如果方法执行失败，返货的对象为null
        if user is not  None:
            userprofile = models.UserProfile.objects.get(user=user)
            if userprofile.enabled:
                #如果账号已启用
                auth_login(request,user)
                #因为用的是 django的验证等，所以要让django知道已经登录，
                return redirect('/index/')
            else:
                message = '账号未启用，请联系管理员'
                return render(request, 'login.html', {"message": message})
        else:
            message = '登陆失败，账号或密码错误'
            return render(request, 'login.html', {'message': message})
    return render(request, 'login.html', locals())


@login_required(login_url='/login/')
def logout(request):
    auth_logout(request)
    #我也需要让django知道我已经退出了
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
    return render(request,'index.html',{'remote_user_bind_host': remote_user_bind_host})


@login_required(login_url='/login/')  #进制未登录直接访问首页
def profile(request):
    pro = models.Profile.objects.filter(user = request.user)
    return render(request,'profile.html',{'pro': pro})
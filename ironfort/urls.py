"""ironfort URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from fort import views
from asset import views as av
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login),  #等于1系列^$ 没有uri就直接跳转到登录页，就是网站默认打开就是登录页
    path('login/', views.login),
    path('index/',views.index),
    path('logout/',views.logout),
    path('profile/',views.profile),
    path('image/',views.update_head),
    #匹配websocket传过来的ws url
    path('host/<int:user_bind_host_id>/',views.connect),
    path('log/',views.get_log),
    #path('host_mgr/cmd/', views.host_mgr,name='batch_cmd'),
    path('upfile/',views.upload_file),
    path('upfile/files/<str:filename>',views.download),

    #资产：
    path('asset/',av.hostlist),
    path('detail/<int:asset_id>',av.detail)
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
#让静态文件的路由 使用settings里的两个值，第二个值默认没有需要自己写，指定静态文件的目录位置
#http://10.211.55.12:8000/static/plugins/jQuery/jquery-2.2.3.min.js
#理解为 走 STATIC_URL匹配的(/static/)   就设定代码目录是 STATIC_ROOT ，好像nginx的 root指定location的代码目录
from django.contrib import admin
from django.apps import apps
from django.utils.text import capfirst
from  . import models

#调整Django菜单顺序为admin注册顺序
def find_app_index(app_label):
    app = apps.get_app_config(app_label)
    main_menu_index = getattr(app, 'main_menu_index', 9999)
    return main_menu_index


def find_model_index(name):
    count = 0
    for model, model_admin in admin.site._registry.items():
        if capfirst(model._meta.verbose_name_plural) == name:
            return count
        else:
            count += 1
    return count


def index_decorator(func):
    def inner(*args, **kwargs):
        templateresponse = func(*args, **kwargs)
        app_list = templateresponse.context_data['app_list']
        app_list.sort(key=lambda r: find_app_index(r['app_label']))
        for app in app_list:
            app['models'].sort(key=lambda x: find_model_index(x['name']))
        return templateresponse

    return inner

admin.site.index = index_decorator(admin.site.index)
admin.site.app_index = index_decorator(admin.site.app_index)

#自定义显示
class HostAdmin(admin.ModelAdmin):
    list_display = ('hostname','ip','port','release','memo')
    list_filter = ('release','port','memo')
    search_fields = ('hostname','ip','memo')

class RemoteUserAdmin(admin.ModelAdmin):
    list_display = ('remote_user_name','password')

class RemoteUserBindHostAdmin(admin.ModelAdmin):
    list_display = ('host','remote_user')
    #search_fields = ('host','remote_user')

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user','user_type','enabled')
    list_filter = ('user_type',)
    search_fields = ('user',)

class UserInfoAdmin(admin.ModelAdmin):
    list_display = ('user','job')
    list_filter = ('job',)
    #search_fields = ('user',)

class GroupAdmin(admin.ModelAdmin):
    list_display = ('group_name',)

admin.site.register(models.Host,HostAdmin)
admin.site.register(models.RemoteUser,RemoteUserAdmin)
admin.site.register(models.RemoteUserBindHost,RemoteUserBindHostAdmin)
admin.site.register(models.UserProfile,UserProfileAdmin)
admin.site.register(models.UserInfo,UserInfoAdmin)
admin.site.register(models.Group,GroupAdmin)
admin.site.register(models.AccessLog)




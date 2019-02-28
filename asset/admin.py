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

# class AssetAdmin(admin.ModelAdmin):
#     list_display = ('name','asset_type')
#     list_filter = ('name','asset_type')
#     search_fields = ('name')
#
# class ServerAdmin(admin.ModelAdmin):
#     list_display = ('asset.name')
#
# class SecurityDeviceAdmin(admin.ModelAdmin):
# class StorageDeviceAdmin(admin.ModelAdmin):
# class NetworkDeviceAdmin(admin.ModelAdmin):
# class SoftwareAdmin(admin.ModelAdmin):
# class IDCAdmin(admin.ModelAdmin):
# class ManufacturerAdmin(admin.ModelAdmin):
# class BusinessUnitAdmin(admin.ModelAdmin):
# class TagAdmin(admin.ModelAdmin):
# class CPUAdmin(admin.ModelAdmin):
# class RAMAdmin(admin.ModelAdmin):
# class DiskAdmin(admin.ModelAdmin):
# class NICAdmin(admin.ModelAdmin):
# class EventLogAdmin(admin.ModelAdmin):

admin.site.register(models.Asset)
admin.site.register(models.BusinessUnit)
admin.site.register(models.CPU)
admin.site.register(models.Disk)
admin.site.register(models.EventLog)
admin.site.register(models.IDC)
admin.site.register(models.Manufacturer)
admin.site.register(models.NetworkDevice)
admin.site.register(models.NIC)
admin.site.register(models.RAM)
admin.site.register(models.SecurityDevice)
admin.site.register(models.Server)
admin.site.register(models.Software)
admin.site.register(models.StorageDevice)
admin.site.register(models.Tag)

from django.contrib import admin
from  . import models


admin.site.register(models.Host)
admin.site.register(models.UserProfile)
admin.site.register(models.Group)
admin.site.register(models.RemoteUser)
admin.site.register(models.RemoteUserBindHost)
admin.site.register(models.Profile)
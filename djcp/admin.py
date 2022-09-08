from django.contrib import admin

# Register your models here.
from djcp import models

admin.site.register(models.GmanagerInfo)
admin.site.register(models.Customer)
admin.site.register(models.CUserInfo)
admin.site.register(models.ProInfo)
admin.site.register(models.ProDate)
admin.site.register(models.BonusUnit)
admin.site.register(models.BonusSystem)

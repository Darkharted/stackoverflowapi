from django.contrib import admin

from account.models import CustomManager, CustomUser

admin.site.register(CustomUser)
# Register your models here.

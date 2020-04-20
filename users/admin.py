from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import User, Notification


# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Notification)
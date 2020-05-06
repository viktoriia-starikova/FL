from django.contrib import admin
from .models import Profile
##Регистрация профиля в админ панели
admin.site.register(Profile)

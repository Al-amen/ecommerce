from django.contrib import admin
from account import models
from django.contrib.auth import get_user_model
User = get_user_model()
# Register your models here.
admin.site.register(models.Profile)
admin.site.register(models.Verification)
admin.site.register(User)

from django.contrib import admin

from apps.users.models import UserProfile
from django.contrib.auth.admin import UserAdmin

# Register your models here.


class UserProfileAdmin(admin.ModelAdmin):
    pass


#admin.site.register(UserProfile, UserAdmin)



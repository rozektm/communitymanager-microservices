from django.contrib import admin
from django.contrib.auth import admin as auth_admin

from communitymanager_3.members.models import Member


@admin.register(Member)
class UserAdmin(auth_admin.UserAdmin):

    list_display = ["first_name", "email"]
    search_fields = ["first_name"]

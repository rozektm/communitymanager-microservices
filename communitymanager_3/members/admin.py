from django.contrib import admin

from communitymanager_3.members.models import (
    Community,
    CommunityAttributes,
    Member,
    Membership,
    Metadata,
)


@admin.register(Metadata)
class MetadataAdmin(admin.ModelAdmin):

    list_display = ["type", "value"]


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):

    list_display = ["name", "email"]


@admin.register(Community)
class CommunityAdmin(admin.ModelAdmin):

    list_display = ["name", "abreviation"]


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):

    list_display = ["level", "community", "member"]


@admin.register(CommunityAttributes)
class CommunityAttributesAdmin(admin.ModelAdmin):

    list_display = ["community", "type", "value"]

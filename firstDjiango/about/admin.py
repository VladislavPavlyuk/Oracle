from django.contrib import admin
from about.models import AboutMember


@admin.register(AboutMember)
class AboutMemberAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "role", "sort_order")
    ordering = ("sort_order", "id")
    search_fields = ("name", "role", "bio")

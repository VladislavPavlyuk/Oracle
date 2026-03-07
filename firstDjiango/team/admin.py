from django.contrib import admin
from team.models import Resume, Notification
from team.models import TeamMember

admin.site.register(TeamMember)
admin.site.register(Resume)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("id", "recipient", "date_created", "is_read")
    list_filter = ("is_read", "date_created", "recipient")

    def change_view(self, request, object_id, form_url="", extra_context=None):
        Notification.objects.filter(pk=object_id, is_read=False).update(is_read=True)
        return super().change_view(request, object_id, form_url, extra_context)

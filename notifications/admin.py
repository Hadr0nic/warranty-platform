from django.contrib import admin
from .models import Notification

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "notif_type", "notif_status", "sent_at", "created_date")
    list_filter = ("notif_type", "notif_status")
    search_fields = ("title", "message", "user__username", "user__email")

    def has_add_permission(self, request):
        # admin0 cannot create notifications via admin panel
        return request.user.role in ["technician", "admin"]

    def has_change_permission(self, request, obj=None):
        # non-editable
        return False

    def has_delete_permission(self, request, obj=None):
        # no-delete
        return request.user.role in ["technician", "admin"]

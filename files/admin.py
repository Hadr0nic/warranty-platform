from django.contrib import admin
from .models import UploadedFile
from django.utils.html import format_html

@admin.register(UploadedFile)
class FilesAdmin(admin.ModelAdmin):
    list_display = ('repair_request', 'user', 'file_type', 'is_minified', 'created_date')
    list_filter = ('file_type', 'is_minified', 'created_date')
    search_fields = ('user__username', 'repair_request__title')
    readonly_fields = ('file_preview',)
    fieldsets = (
        (None, {
            'fields': ('user', 'repair_request', 'file_type', 'file', 'file_url', 'is_minified')
        }),
        ('Preview', {
            'fields': ('file_preview',),
        }),
    )

    def file_preview(self, obj):
        if obj.file and obj.file_type == obj.IMAGE:
            return format_html(
                '<img src="{}" style="max-height:200px;"/>',
                obj.file.url
            )
        return "No preview available"
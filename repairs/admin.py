from django.contrib import admin
from .models import ProductCategory, RepairRequestQuerySet, RepairRequest

@admin.register(ProductCategory)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(RepairRequest)
class RequestAdmin(admin.ModelAdmin):
    list_display = ('title', 'product_category', 'user', 'status', 'created_date', 'updated_date')
    list_filter = ('product_category',)
    search_fields = ('title', 'description')
    list_filter = ('status',)
    ordering = ['-created_date']
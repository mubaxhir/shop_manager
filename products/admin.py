# products/admin.py
from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'sku', 'price', 'inventory_quantity', 'last_updated']
    search_fields = ['name', 'sku']
    list_filter = ['last_updated']

    actions = ['bulk_price_update']

    def bulk_price_update(self, request, queryset):
        for product in queryset:
            product.price *= 1.1
            product.save()
        self.message_user(request, "Prices updated successfully")

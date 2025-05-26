# products/admin.py
from django.contrib import admin
from .models import Product
from django.db import transaction

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'sku', 'price', 'inventory_quantity', 'last_updated']
    search_fields = ['name', 'sku']
    list_filter = ['sku', 'name', 'last_updated']

    actions = ['bulk_price_update', 'bulk_price_decrease']

    @transaction.atomic
    def bulk_increase_prices(self, request, queryset):
        for product in queryset:
            product.price *= 1.10
            product.save()
        self.message_user(request, "Increased prices by 10% for selected products.")
    bulk_increase_prices.short_description = "Increase prices by 10%%"

    @transaction.atomic
    def bulk_price_decrease(self, request, queryset):
        for product in queryset:
            product.price *= 0.9
            product.save()
        self.message_user(request, "Decreased prices by 10%% for selected products.")
    bulk_price_decrease.short_description = "Decrease prices by 10%%"

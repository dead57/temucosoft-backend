from django.contrib import admin
from .models import Supplier, Branch, Category, Product, Inventory

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'sku', 'price', 'company')
    search_fields = ('name', 'sku')

@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('product', 'branch', 'stock')
    list_filter = ('branch',)

admin.site.register(Supplier)
admin.site.register(Branch)
admin.site.register(Category)
from django.contrib import admin
from .models import Product, Category, Supplier, StockLog

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'sku', 'quantity', 'price', 'category', 'supplier', 'low_stock_warning')
    search_fields = ('name', 'sku')
    list_filter = ('category', 'supplier')
    actions = ['calculate_inventory_value']

    def low_stock_warning(self, obj):
        return obj.is_low_stock()  
    low_stock_warning.boolean = True  

    def calculate_inventory_value(self, request, queryset):
        total_value = sum(product.quantity * product.price for product in queryset)
        self.message_user(request, f'Total Inventory Value of selected products: ₹{total_value:.2f}')
    calculate_inventory_value.short_description = "Calculate total inventory value for selected products"

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(StockLog)
class StockLogAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity_changed', 'date_changed', 'reason')
    list_filter = ('product', 'date_changed')
    search_fields = ('product__name', 'reason')

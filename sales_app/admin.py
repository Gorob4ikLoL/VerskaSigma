from django.contrib import admin
from .models import Employee, Product, SalesPlan, Sale


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['user', 'position', 'phone']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'position']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'active']
    list_filter = ['active']
    search_fields = ['name']


@admin.register(SalesPlan)
class SalesPlanAdmin(admin.ModelAdmin):
    list_display = ['product', 'start_date', 'end_date', 'target_amount']
    list_filter = ['start_date', 'end_date', 'product']


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ['employee', 'product', 'quantity', 'date', 'total_price']
    list_filter = ['date', 'employee', 'product']
    date_hierarchy = 'date'

    def total_price(self, obj):
        return obj.total_price

    total_price.short_description = 'Загальна сума'
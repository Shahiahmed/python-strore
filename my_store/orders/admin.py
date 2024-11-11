from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']
    extra = 0  # Убирает лишние пустые строки для добавления новых позиций
    readonly_fields = ['product', 'price', 'quantity']  # Поля только для чтения, если не хотите их редактировать

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'first_name', 'last_name', 'email', 'address',
        'paid', 'created', 'updated', 'get_items'
    ]
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]  # Добавляем OrderItem как инлайн в OrderAdmin

from django.contrib import admin

from order.models import Cart,Order,WishList

admin.site.register(Cart)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'payment_method', 'shipping_status', 'created')
    list_filter = ('shipping_status', 'created')
    search_fields = ('user__username', 'order_id')
    ordering = ('-created',)
    fields = ('user', 'order_items', 'payment_id', 'order_id', 'payment_method', 'shipping_status')
    readonly_fields = ('created',)
    
admin.site.register(WishList)
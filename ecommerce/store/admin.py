from django.contrib import admin
from store import models




class ProductImagesAdmin(admin.StackedInline):
    model = models.ProductImages
    extra = 1  # Optional: Number of empty forms to display for additional images

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImagesAdmin]
    prepopulated_fields = {'slug': ('name',)}  # Automatically populate slug from name
    list_display = ('name', 'category', 'price', 'stock', 'is_stock', 'created')
    list_editable = ('stock',)
    list_filter = ('category', 'is_stock')
    search_fields = ('name', 'category__name')


@admin.register(models.VariationValue)
class VariationValueAdmin(admin.ModelAdmin):
    list_display = ('product', 'variation', 'name', 'price', 'stock', 'is_stock')
    list_filter = ('variation', 'is_stock')
    search_fields = ('name', 'product__name')
    list_editable = ('price', 'stock', 'is_stock')
    
    def save_model(self, request, obj, form, change):
        """Customize save to handle stock status based on stock quantity."""
        if obj.stock == 0:
            obj.is_stock = False
        else:
            obj.is_stock = True
        super().save_model(request, obj, form, change)

@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'total_stock', 'created')
    search_fields = ('name',)
    list_filter = ('parent',)

    def total_stock(self, obj):
        """Display total stock for the category and its subcategories."""
        return obj.get_total_stock()

    total_stock.short_description = "Total Stock"



#admin.site.register(models.Product,ProductAdmin)
admin.site.register(models.Banner)
admin.site.register(models.MyLogo)
admin.site.register(models.MyFavicon)
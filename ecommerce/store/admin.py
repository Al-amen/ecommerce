from django.contrib import admin
from store import models



class ProductImagesAdmin(admin.StackedInline):
    model = models.ProductImages
   

    



class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImagesAdmin]
    prepopulated_fields = {'slug':('name',)}


admin.site.register(models.Category)
admin.site.register(models.Product,ProductAdmin)
admin.site.register(models.VariationValue)
admin.site.register(models.Banner)
admin.site.register(models.MyLogo)
admin.site.register(models.MyFavicon)
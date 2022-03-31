from django.contrib import admin

from .models import Products, Favorites, Category


class ProductsAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'product_url', 'product_image',
                    'product_nutriscore', 'product_category')
    list_filter = ('product_name', 'product_nutriscore', 'product_category')
    search_fields = ('product_name', 'product_nutriscore', 'product_category')


class FavoritesAdmin(admin.ModelAdmin):
    list_display = ('user', 'product')
    list_filter = ('user', 'product')
    search_fields = ('user', 'product')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name',)
    list_filter = ('category_name',)
    search_fields = ('category_name',)


admin.site.register(Products, ProductsAdmin)
admin.site.register(Favorites, FavoritesAdmin)
admin.site.register(Category, CategoryAdmin)

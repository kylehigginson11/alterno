# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from alternosite.models import Category, SubCategory, ProductLine, Brand, Product


class CategoryAdmin(admin.ModelAdmin):
    fields = ('name', )
    list_display = ('name', )


class SubCategoryAdmin(admin.ModelAdmin):
    fields = ('name', 'category')
    list_display = ('name', 'category')


class ProductLineAdmin(admin.ModelAdmin):
    fields = ('name', 'sub_category')
    list_display = ('name', 'sub_category')


class BrandAdmin(admin.ModelAdmin):
    fields = ('name',)
    list_display = ('name',)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'product_line', 'approved')


admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(ProductLine, ProductLineAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Product, ProductAdmin)
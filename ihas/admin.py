from django.contrib import admin
from .models import Category, Uav, Rental


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'category_slug': ('category_name',)}


class UavAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'brand', 'category', 'model', 'year', 'weight', 'features', 'price', 'status',)
    search_fields = ('name', 'brand', 'category', 'model', 'year', 'weight', 'features', 'price', 'status',)
    list_editable = ('status',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Uav, UavAdmin)
admin.site.register(Rental)


from django.contrib import admin
from .models import Collection, Product

# Register your models here.
admin.site.register(Collection)
# admin.site.register(Product) # simple way to register a model in the admin site. to edit the admin interface, we need to create a ModelAdmin class.

# we can also customize the admin interface by creating a ModelAdmin class and registering it with the model.
@admin.register(Product) # this is a decorator that does the same thing as admin.site.register(Product, ProductAdmin). it is just a cleaner way to do it.
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'unit_price', 'collection'] # fields to display in the admin list view
    list_filter = ['collection'] # fields to filter in the admin list view
    list_editable = ['unit_price'] # fields to edit in the admin list view
    list_per_page = 10 # number of items to display per page in the admin list view

# Note: ModelAdmin vs admin.site.register:
# ModelAdmin is a class that defines the admin interface for a model. it is used to customize the admin interface.
# admin.site.register is a function that registers a model with the admin site. it is used to make a model available in the admin site.
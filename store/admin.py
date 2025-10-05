from django.contrib import admin
from .models import Collection, Product, Customer, Order

# Register your models here.
admin.site.register(Collection)
# admin.site.register(Product) # simple way to register a model in the admin site. to edit the admin interface, we need to create a ModelAdmin class.

# we can also customize the admin interface by creating a ModelAdmin class and registering it with the model.
@admin.register(Product) # this is a decorator that does the same thing as admin.site.register(Product, ProductAdmin). it is just a cleaner way to do it.
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'unit_price', 'inventory', 'inventory_status', 'collection', 'collection_title'] # here, inventory_status is a custom method defined below. it is not a field in the model. it calls the method and displays the result in the admin list view. here collection is a foreign key field, django automatically displays the related object's __str__ method.
    list_filter = ['collection'] # fields to filter in the admin list view
    list_editable = ['unit_price'] # fields to edit in the admin list view
    list_per_page = 10 # number of items to display per page in the admin list view
    list_select_related = ['collection'] # to optimize the query and reduce the number of queries to the database. it will use a SQL join to fetch the related objects in a single query instead of multiple queries.

    @admin.display(ordering='inventory') # this decorator is used to customize the display of the method in the admin list view. ordering parameter is used to specify the field to order by when the column header is clicked.
    def inventory_status(self, product): # custom method to display inventory status. it takes the product object as a parameter.
        if product.inventory < 10:
            return 'Low'
        return 'OK'
    
    def collection_title(self, product): # custom method to display the collection title. it takes the product object as a parameter.
        return product.collection.title

# Note: ModelAdmin vs admin.site.register:
# ModelAdmin is a class that defines the admin interface for a model. it is used to customize the admin interface.
# admin.site.register is a function that registers a model with the admin site. it is used to make a model available in the admin site.



@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership']
    list_editable = ['membership']
    list_per_page = 10
    ordering = ['first_name', 'last_name'] # ordering in ModelAdmin class is used to define the ordering for the model in the admin site only. it will not affect the ordering in the shell.
# Note: editing in admin.py => ModelAdmin class is for customizing the admin interface,
# while editing in models.py => Meta class is for configuring model behavior (like ordering, verbose_name, etc.)



@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'placed_at', 'customer_name']
    list_per_page = 10
    list_select_related = ['customer'] # to optimize the query and reduce the number of queries to the database. it will use a SQL join to fetch the related objects in a single query instead of multiple queries.

    # two way to display related object's field in the admin list view:
    # 1. using a custom method (as shown below)
    # 2. in models.py, __str__ method 
    def customer_name(self, order): # custom method to display the customer name. it takes the order object as a parameter.
        return order.customer.first_name # we can access the related object's fields using the foreign key field.
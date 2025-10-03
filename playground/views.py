from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.db.models import Q, F
from django.db.models import Count, Min, Max, Avg, Sum, Value
from store.models import Product, Customer, Collection, Order, OrderItem


def say_hello(request):
# The following line uses Django's ORM (Object-Relational Mapper) to fetch data from the database.
# 
# Product.objects.all() does NOT immediately fetch all products from the database.
# Instead, it creates a QuerySet, which is a lazy object representing the query.
# 
# - "Product" is the model class representing a table in the database.
# - ".objects" is the model manager that provides access to ORM query methods.
# - ".all()" creates a QuerySet for all rows in the "Product" table.
#
# Under the hood:
# - Django builds a SQL query (like "SELECT * FROM store_product") but does NOT run it yet.
# - The actual database query happens only when you iterate over the QuerySet (e.g., in a for loop),
#   convert it to a list, or otherwise force evaluation.
# - This lazy evaluation makes queries efficient, as you can further filter or slice the QuerySet before hitting the database.
#
# Example:
#   query_set = Product.objects.all()  # No database access yet!
#   for product in query_set:          # Database query runs here, fetching products one by one.

    query_set = Product.objects.all()
    query_set = query_set.filter(title='Bread Ww Cluster').order_by('-unit_price')  # Further filtering the QuerySet (still no DB access)

    # Here in query_set = list(query_set)  Executed SQL

# SELECT "store_product"."id",
#        "store_product"."title",
#        "store_product"."slug",
#        "store_product"."description",
#        "store_product"."unit_price",
#        "store_product"."inventory",
#        "store_product"."last_update",
#        "store_product"."collection_id"
#   FROM "store_product"
#  WHERE "store_product"."title" = 'Bread Ww Cluster'
#  ORDER BY "store_product"."unit_price" DESC
    
    for product in query_set:
        print(product)


# Retrieving a single object by primary key (id)
    # if you try to get a product that does not exist, it will raise an exception
    try:
        # Fetches a single product with primary key 1 (executes SQL immediately). pk is shorthand for primary key. in django pk automatically maps to id field
        product = Product.objects.get(pk=1) 
        # Both are same. id and pk are interchangeable in this context. id is the actual field name in the model, while pk is a more general term that always refers to the primary key of the model.
        product = Product.objects.get(id=1)
    
    except ObjectDoesNotExist:
        pass
    
    exist_bool = Product.objects.filter(id=1).exists()  # Returns True if a product with id=1 exists, otherwise False
    product_2 = Product.objects.filter(id=0).first()  # Returns None if no match is found, avoiding exception


    # Filtering objects with LooksUp. field lookups examples: exact, iexact, contains, icontains, in, gt, gte, lt, lte, startswith, istartswith, endswith, iendswith, range, date, year, month, day, week_day, isnull, search, regex, iregex are available to use.
    # Field lookups are used to create more complex queries by specifying conditions on model fields.
    # queryset_filter = Product.objects.filter(unit_price__gt =20)
    queryset_filter = Product.objects.filter(unit_price__range =(20,30))
    # we can use multiple filters like startswith and endswith, etc.
    queryset_filter2 = Product.objects.filter(title__contains='coffee')  # Case-sensitive contains
    queryset_filter3 = Product.objects.filter(title__icontains='coffee')  # Case-insensitive contains
    queryset_filter4 = Product.objects.filter(title__istartswith='coffee')  # Case-insensitive startswith
    queryset_filter5 = Product.objects.filter(last_update__year='2021')  # Products updated in the year 2023
    queryset_filter6 = Product.objects.filter(description__isnull=True)  # Products with no description


    queryset_filter7 = Customer.objects.filter(email__endswith='.com')  # Customers with email ending in .com
    queryset_filter8 = Product.objects.filter(inventory__lt=10)  # Products with inventory less than 10
    queryset_filter9 = Order.objects.filter(pk=1) # Orders with primary key 1

    # Complex lookups using Q objects for OR conditions
    # inventory < 10 AND unit_price < 20
    queryset_filter10 = Product.objects.filter(inventory__lt=10, unit_price__lt=20)  # AND condition
    queryset_filter11 = Product.objects.filter(inventory__lt=10).filter(unit_price__lt=20)  # Chained filters (also AND condition). filter returns a query set. when call by list(name) then queryset evaluated.
    
    # inventory < 10 OR unit_price < 20
    queryset_filter12 = Product.objects.filter(Q(inventory__lt=10) | Q(unit_price__lt=20))  # OR condition using Q objects
    queryset_filter13 = Product.objects.filter(Q(inventory__lt=10) & Q(unit_price__lt=20))  # AND condition using Q objects
    queryset_filter14 = Product.objects.filter(Q(inventory__lt=10) & ~Q(unit_price__lt=20))  # inventory < 10 AND NOT (unit_price < 20) using Q objects

    # Referencing related fields using F objects
    # Products: inventory = unit_price
    # queryset_filter15 = Product.objects.filter(inventory=unit_price) # This will raise an error because unit_price is not defined in this scope. To reference model fields, we should use F objects from django.db.models.
    # queryset_filter16 = Product.objects.filter(inventory=F('unit_price'))  # Using F objects to reference model fields


# F Object
# Purpose: Reference model field values directly in queries and updates.
# Use Case: When you want to compare a field to another field, or perform arithmetic using field values.
# Example: Find products where inventory equals unit_price:

# Q Object
# Purpose: Build complex queries with AND, OR, and NOT logic.
# Use Case: When you need to combine multiple conditions, especially with OR or NOT.
# Example: Find products where inventory < 10 OR unit_price < 20:

    # Sorting
    queryset_filter17 = Product.objects.order_by('title') # Ascending order by title
    queryset_filter18 = Product.objects.order_by('title', '-unit_price') # Ascending by title, then descending by unit_price
    queryset_filter19 = Product.objects.order_by('title', '-unit_price').reverse() # Reverse the order of the previous sorting
    
    queryset_filter20 = Product.objects.order_by('unit_price')[0] 
    queryset_filter21 = Product.objects.earliest('unit_price') # returns the object with the lowest unit_price


    # Limiting results
    queryset_filter22 = Product.objects.all()[:5]  # First 5 products
    queryset_filter23 = Product.objects.all()[5:10]


    # Selecting fields for query (to optimize performance)
    # by default, Django retrieves all fields of a model when you query it.
    # However, if you only need specific fields, you can use .only() or .values() to limit the fields fetched from the database.

    queryset_filter24 = Product.objects.values('id', 'title')  # Returns dictionaries with only 'id' and 'title' fields
    queryset_filter25 = Product.objects.values('id', 'title', 'collection__title')  # Including related field 'collection.title'. it will return type of dictionary
    queryset_filter26 = Product.objects.values_list('id', 'title', 'collection__title')  # Returns tuples with 'id', 'title', and 'collection_id' fields

    # Select Product that have been ordered and sort by title
    queryset = OrderItem.objects.values('product_id').distinct() # you can call product_id or product__id both are same. but product_id is faster because it does not involve a join. and distinct() is used to eliminate duplicate product ids.
    queryset2 = Product.objects.filter(id__in=queryset).order_by('title') # Select Products that have been ordered and sort by title. here id__in is used to filter products whose id is in the list of product ids from the OrderItem queryset.
    
    # values() vs only()
    # .values() returns dictionaries with only the specified fields, while .only() returns model
    queryset3 = Product.objects.only('id', 'title')  # Fetches only 'id' and 'title' fields, other fields are deferred until accessed
    ## Warning: Using .only() can lead to additional database queries if you access deferred fields later, so use it judiciously. only use it when you are sure you won't need the other fields.
    ## IF you dont know what you are doing, you end up with N+1 query problem. so be careful when using only().

    queryset4 = Product.objects.defer('description')  # Fetches all fields except 'description', which is deferred until accessed
    ## Warning: Similar to .only(), using .defer() can lead to additional queries if deferred fields are accessed later. so use it judiciously.
    ## if you use for loop and inside the loop you access the deferred field, it will make a query for each iteration. so be careful when using defer().
    

    ## Selecting related objects to avoid N+1 query problem
    queryset5 = Product.objects.all()  # This will cause N+1 query problem if you access related fields in a loop. here this will call only all products query. but when you access related fields like collection.title in a loop, it will make a query for each product to fetch the related collection.
    queryset6 = Product.objects.select_related('collection').all()  # This will fetch related collection in the same query using a SQL join. use select_related for ForeignKey and OneToOne relationships only. it is faster because it uses a SQL join and preloads the related objects in a single query.
    # use select_related when you know you will need the related object and you want to avoid additional queries.
    # and select_related (1) is used for single-valued relationships (ForeignKey, OneToOneField). 
    # if you have multi-valued relationships (ManyToManyField, reverse ForeignKey), use prefetch_related instead.

    queryset7 = Product.objects.prefetch_related('promotions').all()  # This will fetch related promotions in a separate query and join them in Python. use prefetch_related for ManyToMany and reverse ForeignKey relationships. it is useful when you have a lot of related objects and you want to avoid loading them all at once.
    # use prefetch_related when you have multi-valued relationships and you want to avoid loading

    # Get the last 5 orders with their customer and items (include product)
    queryset8 = Order.objects.select_related('customer').prefetch_related('orderitem_set__product').order_by('-placed_at')[:5] # here orderitem_set is the reverse relationship from OrderItem to Order. django automatically creates a reverse relationship for ForeignKey fields. and you can access it using the model name in lowercase followed by _set. you can change the name of the reverse relationship by adding related_name parameter in ForeignKey field. here we are using double underscore to access the product field of the OrderItem model. this will prefetch all the products related to the order items in a separate query and join them in python. this will avoid N+1 query problem when you access orderitem_set and product fields in a loop.

    # Aggregating objects.
    # from django.db.models import Count, Min, Max, Avg, Sum
    result = Product.objects.aggregate(Count('id')) # Total number of products. it will return a dictionary with the key as id__count and value as the count of products not the queryset.
    result2 = Product.objects.aggregate(count=Count('id')) # Total number of products with custom key name. it will return a dictionary with the key as count and value as the count of products.
    result3 = Product.objects.aggregate(count=Count('id'), min_price=Min('unit_price')) # Total number of products and minimum unit price. it will return a dictionary with the keys as count and min_price and values as the count of products and minimum unit price respectively.

    # Annotating objects. (similar to aggregate but it returns a queryset with the aggregated values for each object in the queryset)
    # we need to pass an expression to annotate() method. expression can be an aggregate function or a F object or a combination of both.
    # example of all expressions: Count, Sum, Avg, Max, Min, F, Value, Case, When, Q, etc.
    result4 = Customer.objects.annotate(is_new=Value(True)) # Annotate each customer with a new field 'is_new' set to True. here Value(True) is used to create a constant value for the new field.
    result5 = Customer.objects.annotate(new_id=F('id')+1) # Annotate each customer with a new field 'new_id' which is id + 1. here F('id') is used to reference the id field of the Customer model.



    return render(request, 'hello.html', {'name': 'Arafat', 'products': list(result5)})

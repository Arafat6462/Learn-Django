from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.db.models import Q
from store.models import Product, Customer, Collection, Order


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
    # filtered_products = Product.objects.filter(unit_price__gt =20)
    filtered_products = Product.objects.filter(unit_price__range =(20,30))
    # we can use multiple filters like startswith and endswith, etc.
    filtered_products2 = Product.objects.filter(title__contains='coffee')  # Case-sensitive contains
    filtered_products3 = Product.objects.filter(title__icontains='coffee')  # Case-insensitive contains
    filtered_products4 = Product.objects.filter(title__istartswith='coffee')  # Case-insensitive startswith
    filtered_products5 = Product.objects.filter(last_update__year='2021')  # Products updated in the year 2023
    filtered_products6 = Product.objects.filter(description__isnull=True)  # Products with no description


    filtered_products7 = Customer.objects.filter(email__endswith='.com')  # Customers with email ending in .com
    filtered_products8 = Product.objects.filter(inventory__lt=10)  # Products with inventory less than 10
    filtered_products9 = Order.objects.filter(pk=1) # Orders with primary key 1

    # Complex lookups using Q objects for OR conditions
    # inventory < 10 AND unit_price < 20
    filtered_products10 = Product.objects.filter(inventory__lt=10, unit_price__lt=20)  # AND condition
    filtered_products11 = Product.objects.filter(inventory__lt=10).filter(unit_price__lt=20)  # Chained filters (also AND condition). filter returns a query set. when call by list(name) then queryset evaluated.
    
    # inventory < 10 OR unit_price < 20
    filtered_products12 = Product.objects.filter(Q(inventory__lt=10) | Q(unit_price__lt=20))  # OR condition using Q objects
    filtered_products13 = Product.objects.filter(Q(inventory__lt=10) & Q(unit_price__lt=20))  # AND condition using Q objects
    filtered_products14 = Product.objects.filter(Q(inventory_lt=10) & ~Q(unit_price__lt=20))  # inventory < 10 AND NOT (unit_price < 20) using Q objects




    

    print(filtered_products)


    return render(request, 'hello.html', {'name': 'Arafat', 'products': list(filtered_products12)})

from django.shortcuts import render
from django.http import HttpResponse
from store.models import Product


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

    return render(request, 'hello.html', {'name': 'Arafat'})

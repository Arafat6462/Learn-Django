from django.db import models

class Collection(models.Model):
    title = models.CharField(max_length=255)

class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField()
    # Product_set will be created automatically in Product model
    # django automatically adds reverse relationship in the related model
    # products = reverse relationship from Product model will be created automatically as 'promotions_set' unless specified otherwise in Product model
    products = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, related_name='+')
# Create your models here.
class Product(models.Model):
    # in django, primary key is automatically added as id field if not specified otherwise
    # sku = models.CharField(max_length=10, primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    inventory = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT)
    Promotions = models.ManyToManyField(Promotion)

class Customer(models.Model):
    MEMBERSHIP_BRONZE = 'B'
    MEMBERSHIP_SILVER = 'S'
    MEMBERSHIP_GOLD = 'G'

    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_BRONZE, 'Bronze'),
        (MEMBERSHIP_SILVER, 'Silver'),
        (MEMBERSHIP_GOLD, 'Gold'),
    ]
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=255)
    birth_date = models.DateField(null=True)
    membership = models.CharField(max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BRONZE)
    


class Order(models.Model):
    PAYMENT_STATUS_PENDING = 'P'
    PAYMENT_STATUS_COMPLETE = 'C'
    PAYMENT_STATUS_FAILED = 'F'

    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STATUS_PENDING, 'Pending'),
        (PAYMENT_STATUS_COMPLETE, 'Complete'),
        (PAYMENT_STATUS_FAILED, 'Failed'),
    ]

    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=1, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_STATUS_PENDING)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)

class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()


class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)

    # This line creates a one-to-one relationship between your model and the Customer model.
    # Each instance of your model is linked to exactly one Customer.
    # If the Customer is deleted, the related instance is also deleted (CASCADE).
    # The field is also set as the primary key for this model.
    # customer = models.OneToOneField(Customer, on_delete=models.CASCADE, primary_key=True)
    
    # This line creates a many-to-one relationship (ForeignKey) to the Customer model.
    # Multiple instances of your model can be linked to the same Customer.
    # If the Customer is deleted, all related instances are also deleted (CASCADE).
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

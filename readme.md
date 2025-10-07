# Django Learning Notes & Cheat Sheet 📚

A comprehensive guide to Django concepts, patterns, and best practices.

---

## Table of Contents
1. [Django Architecture](#django-architecture)
2. [Models](#models)
3. [Views](#views)
4. [Templates](#templates)
5. [URLs](#urls)
6. [Django Admin](#django-admin)
7. [Database & ORM](#database--orm)
8. [Forms](#forms)
9. [Authentication & Authorization](#authentication--authorization)
10. [Static Files & Media](#static-files--media)
11. [Deployment](#deployment)
12. [Best Practices](#best-practices)

---

## Django Architecture

### MVT Pattern (Model-View-Template)
```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│    Model    │    │    View     │    │  Template   │
│ (Database)  │◄──►│ (Logic)     │◄──►│    (UI)     │
│             │    │             │    │             │
└─────────────┘    └─────────────┘    └─────────────┘
```

### Request-Response Flow
```
1. User requests URL
2. Django URLconf routes to view
3. View processes request
4. View queries Model (if needed)
5. View renders Template with data
6. Response sent to user
```

### Project Structure
```
myproject/
├── myproject/          # Project package
│   ├── __init__.py
│   ├── settings.py     # Configuration
│   ├── urls.py         # Main URL configuration
│   ├── wsgi.py         # WSGI application
│   └── asgi.py         # ASGI application
├── myapp/              # Application package
│   ├── migrations/     # Database migrations
│   ├── __init__.py
│   ├── admin.py        # Admin configuration
│   ├── apps.py         # App configuration
│   ├── models.py       # Data models
│   ├── views.py        # View functions/classes
│   ├── urls.py         # App URL patterns
│   └── tests.py        # Unit tests
├── templates/          # HTML templates
├── static/             # CSS, JS, images
└── manage.py          # Management script
```

---

## Models

### Model Definition
```python
from django.db import models
from django.core.validators import MinValueValidator

class Product(models.Model):
    # Field types
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    # Relationships
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    tags = models.ManyToManyField('Tag', blank=True)
    
    # Validation
    price = models.DecimalField(
        validators=[MinValueValidator(0.01)]
    )
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Products'
```

### Field Types Quick Reference
```python
# Text Fields
CharField(max_length=255)          # Short text
TextField()                        # Long text
SlugField()                        # URL-friendly text
EmailField()                       # Email validation

# Numeric Fields
IntegerField()                     # Integer
PositiveIntegerField()             # Positive integer
DecimalField(max_digits=10, decimal_places=2)  # Decimal
FloatField()                       # Float

# Date/Time Fields
DateField()                        # Date only
TimeField()                        # Time only
DateTimeField()                    # Date and time
DateTimeField(auto_now_add=True)   # Set on creation
DateTimeField(auto_now=True)       # Update on save

# Boolean
BooleanField()                     # True/False
BooleanField(default=True)         # With default

# File Fields
FileField(upload_to='uploads/')    # File upload
ImageField(upload_to='images/')    # Image upload

# Choice Fields
STATUS_CHOICES = [
    ('draft', 'Draft'),
    ('published', 'Published'),
]
status = models.CharField(max_length=20, choices=STATUS_CHOICES)
```

### Relationships
```python
# One-to-Many (ForeignKey)
class Category(models.Model):
    name = models.CharField(max_length=100)

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    # Creates: product.category, category.product_set

# Many-to-Many
class Tag(models.Model):
    name = models.CharField(max_length=50)

class Product(models.Model):
    tags = models.ManyToManyField(Tag, blank=True)
    # Creates: product.tags, tag.product_set

# One-to-One
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Creates: profile.user, user.profile
```

### on_delete Options
```python
models.CASCADE          # Delete related objects
models.PROTECT          # Prevent deletion
models.SET_NULL         # Set to NULL (requires null=True)
models.SET_DEFAULT      # Set to default value
models.SET()            # Set to specific value
models.DO_NOTHING       # Do nothing (may cause integrity errors)
```

### Model Methods
```python
class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        """String representation"""
        return self.name
    
    def get_absolute_url(self):
        """URL for this object"""
        return reverse('product-detail', args=[str(self.id)])
    
    @property
    def is_expensive(self):
        """Custom property"""
        return self.price > 100
    
    def save(self, *args, **kwargs):
        """Override save method"""
        # Custom logic before saving
        super().save(*args, **kwargs)
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        unique_together = ['name', 'category']
        indexes = [
            models.Index(fields=['name']),
        ]
```

---

## Database & ORM

### QuerySet Operations
```python
# Basic queries
Product.objects.all()                    # All objects
Product.objects.get(id=1)               # Single object
Product.objects.filter(price__gt=100)   # Filter objects
Product.objects.exclude(is_active=False) # Exclude objects
Product.objects.first()                 # First object
Product.objects.last()                  # Last object
Product.objects.count()                 # Count objects

# Field lookups
Product.objects.filter(name__icontains='phone')  # Case-insensitive contains
Product.objects.filter(price__gte=50)           # Greater than or equal
Product.objects.filter(created_at__year=2024)   # Year lookup
Product.objects.filter(category__name='Electronics')  # Related field

# Common lookups
__exact         # Exact match
__iexact        # Case-insensitive exact
__contains      # Contains substring
__icontains     # Case-insensitive contains
__startswith    # Starts with
__endswith      # Ends with
__gt, __gte     # Greater than, greater than or equal
__lt, __lte     # Less than, less than or equal
__in            # In list
__isnull        # Is null
__range         # Between values
```

### Advanced Queries
```python
from django.db.models import Q, F, Count, Sum, Avg

# Q objects (complex lookups)
Product.objects.filter(
    Q(name__icontains='phone') | Q(name__icontains='tablet')
)

# F objects (field references)
Product.objects.filter(price__gt=F('cost') * 1.5)

# Annotations
Product.objects.annotate(
    total_orders=Count('orderitem'),
    avg_rating=Avg('reviews__rating')
)

# Aggregations
from django.db.models import Count, Sum, Avg, Max, Min
Product.objects.aggregate(
    total_products=Count('id'),
    avg_price=Avg('price'),
    max_price=Max('price')
)

# Select related (optimize foreign keys)
products = Product.objects.select_related('category')

# Prefetch related (optimize reverse foreign keys)
categories = Category.objects.prefetch_related('product_set')

# Raw SQL (when needed)
Product.objects.raw('SELECT * FROM store_product WHERE price > %s', [100])
```

### Migrations
```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Show migrations
python manage.py showmigrations

# Create empty migration
python manage.py makemigrations --empty myapp

# Rollback migration
python manage.py migrate myapp 0001

# SQL for migration
python manage.py sqlmigrate myapp 0001
```

---

## Views

### Function-Based Views (FBV)
```python
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required

def product_list(request):
    """List all products"""
    products = Product.objects.all()
    return render(request, 'products/list.html', {'products': products})

def product_detail(request, pk):
    """Product detail view"""
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'products/detail.html', {'product': product})

@login_required
def product_create(request):
    """Create new product"""
    if request.method == 'POST':
        # Handle form submission
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save()
            return redirect('product-detail', pk=product.pk)
    else:
        form = ProductForm()
    
    return render(request, 'products/form.html', {'form': form})

def api_products(request):
    """JSON API response"""
    products = Product.objects.all()
    data = [{'id': p.id, 'name': p.name, 'price': str(p.price)} for p in products]
    return JsonResponse({'products': data})
```

### Class-Based Views (CBV)
```python
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

class ProductListView(ListView):
    model = Product
    template_name = 'products/list.html'
    context_object_name = 'products'
    paginate_by = 10
    
    def get_queryset(self):
        return Product.objects.filter(is_active=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/detail.html'
    context_object_name = 'product'

class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    fields = ['name', 'price', 'description', 'category']
    template_name = 'products/form.html'
    success_url = reverse_lazy('product-list')
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    fields = ['name', 'price', 'description', 'category']
    template_name = 'products/form.html'

class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'products/confirm_delete.html'
    success_url = reverse_lazy('product-list')
```

### View Decorators
```python
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.http import require_http_methods
from django.views.decorators.cache import cache_page

@login_required
@permission_required('store.add_product')
@require_http_methods(["GET", "POST"])
@cache_page(60 * 15)  # Cache for 15 minutes
def my_view(request):
    pass
```

---

## URLs

### URL Configuration
```python
# myproject/urls.py (main URLconf)
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('store.urls')),
    path('api/', include('api.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# store/urls.py (app URLs)
from django.urls import path
from . import views

app_name = 'store'  # Namespace

urlpatterns = [
    path('', views.ProductListView.as_view(), name='product-list'),
    path('products/<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('products/new/', views.ProductCreateView.as_view(), name='product-create'),
    path('products/<int:pk>/edit/', views.ProductUpdateView.as_view(), name='product-update'),
    path('products/<int:pk>/delete/', views.ProductDeleteView.as_view(), name='product-delete'),
    path('categories/<slug:slug>/', views.category_products, name='category-products'),
]
```

### URL Patterns
```python
# Basic patterns
path('products/', views.product_list, name='product-list')
path('products/<int:pk>/', views.product_detail, name='product-detail')
path('categories/<slug:slug>/', views.category_detail, name='category-detail')

# Path converters
<int:pk>        # Integer
<str:name>      # String (default)
<slug:slug>     # Slug (letters, numbers, hyphens, underscores)
<uuid:id>       # UUID

# Regular expressions (re_path)
from django.urls import re_path
re_path(r'^products/(?P<year>[0-9]{4})/$', views.year_archive, name='year-archive')
```

### Reverse URL Resolution
```python
from django.urls import reverse
from django.shortcuts import redirect

# In views
def my_view(request):
    url = reverse('store:product-detail', args=[1])
    return redirect('store:product-list')

# In templates
{% url 'store:product-detail' product.pk %}
{% url 'store:category-products' category.slug %}

# With namespaces
reverse('store:product-list')
reverse('admin:store_product_changelist')
```

---

## Templates

### Template Syntax
```html
<!-- Variables -->
{{ product.name }}
{{ product.price|floatformat:2 }}
{{ user.first_name|default:"Anonymous" }}

<!-- Tags -->
{% for product in products %}
    <div>{{ product.name }}</div>
{% empty %}
    <p>No products found.</p>
{% endfor %}

{% if user.is_authenticated %}
    <p>Welcome, {{ user.username }}!</p>
{% else %}
    <p>Please log in.</p>
{% endif %}

<!-- Comments -->
{# This is a comment #}
{% comment %}
    Multi-line comment
{% endcomment %}
```

### Template Inheritance
```html
<!-- base.html -->
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}My Site{% endblock %}</title>
    {% load static %}
    <link rel="stylesheet" href="{% static 'css/style.css' %}">
</head>
<body>
    <nav>
        {% block nav %}
            <a href="{% url 'store:product-list' %}">Products</a>
        {% endblock %}
    </nav>
    
    <main>
        {% block content %}
        {% endblock %}
    </main>
    
    <footer>
        {% block footer %}
            <p>&copy; 2024 My Company</p>
        {% endblock %}
    </footer>
</body>
</html>

<!-- product_list.html -->
{% extends 'base.html' %}
{% load static %}

{% block title %}Products - {{ block.super }}{% endblock %}

{% block content %}
    <h1>Products</h1>
    {% for product in products %}
        <div class="product">
            <h2>{{ product.name }}</h2>
            <p>${{ product.price }}</p>
            <a href="{% url 'store:product-detail' product.pk %}">View Details</a>
        </div>
    {% endfor %}
    
    {% include 'partials/pagination.html' %}
{% endblock %}
```

### Common Template Filters
```html
<!-- String filters -->
{{ name|upper }}           <!-- UPPERCASE -->
{{ name|lower }}           <!-- lowercase -->
{{ name|title }}           <!-- Title Case -->
{{ name|capfirst }}        <!-- Capitalize first -->
{{ text|truncatewords:10 }} <!-- Truncate to 10 words -->
{{ text|slice:":100" }}    <!-- First 100 characters -->

<!-- Number filters -->
{{ price|floatformat:2 }}  <!-- 2 decimal places -->
{{ number|add:5 }}         <!-- Add 5 -->

<!-- Date filters -->
{{ date|date:"Y-m-d" }}    <!-- 2024-01-01 -->
{{ date|timesince }}       <!-- "2 hours ago" -->

<!-- List filters -->
{{ list|length }}          <!-- Length of list -->
{{ list|first }}           <!-- First item -->
{{ list|last }}            <!-- Last item -->
{{ list|join:", " }}       <!-- Join with comma -->

<!-- Default values -->
{{ value|default:"N/A" }}  <!-- Show "N/A" if empty -->
{{ value|yesno:"Yes,No,Maybe" }} <!-- Boolean formatting -->
```

### Custom Template Tags and Filters
```python
# store/templatetags/store_extras.py
from django import template

register = template.Library()

@register.filter
def currency(value):
    """Format as currency"""
    return f"${value:.2f}"

@register.simple_tag
def get_products(category=None):
    """Get products, optionally filtered by category"""
    if category:
        return Product.objects.filter(category=category)
    return Product.objects.all()

@register.inclusion_tag('partials/product_card.html')
def product_card(product):
    """Render product card"""
    return {'product': product}

# In template
{% load store_extras %}
{{ product.price|currency }}
{% get_products category as products %}
{% product_card product %}
```

---

## Django Admin

### Basic Admin Registration
```python
# admin.py
from django.contrib import admin
from .models import Product, Category

# Simple registration
admin.site.register(Product)

# Custom admin class
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'product_count']
    search_fields = ['name']
    
    def product_count(self, obj):
        return obj.product_set.count()
```

### Advanced Admin Configuration
```python
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # List view
    list_display = ['name', 'price', 'category', 'is_active', 'created_at']
    list_filter = ['category', 'is_active', 'created_at']
    list_editable = ['price', 'is_active']
    search_fields = ['name', 'description']
    list_per_page = 25
    
    # Form view
    fields = ['name', 'category', 'price', 'description', 'is_active']
    readonly_fields = ['created_at', 'updated_at']
    prepopulated_fields = {'slug': ['name']}
    autocomplete_fields = ['category']
    
    # Filters
    date_hierarchy = 'created_at'
    
    # Actions
    actions = ['make_active', 'make_inactive']
    
    def make_active(self, request, queryset):
        queryset.update(is_active=True)
    make_active.short_description = "Mark selected products as active"
    
    # Custom methods
    @admin.display(ordering='price', description='Price (USD)')
    def price_display(self, obj):
        return f"${obj.price:.2f}"
    
    # Optimize queries
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('category')
```

### Inline Administration
```python
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    autocomplete_fields = ['product']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'status', 'created_at']
    inlines = [OrderItemInline]
    autocomplete_fields = ['customer']
```

### Custom Admin Actions
```python
@admin.action(description='Export selected products to CSV')
def export_as_csv(modeladmin, request, queryset):
    import csv
    from django.http import HttpResponse
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="products.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Name', 'Price', 'Category'])
    
    for product in queryset:
        writer.writerow([product.name, product.price, product.category.name])
    
    return response
```

---

## Forms

### Form Definition
```python
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'description', 'category']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'price': forms.NumberInput(attrs={'step': '0.01'}),
        }
    
    def clean_price(self):
        price = self.cleaned_data['price']
        if price <= 0:
            raise forms.ValidationError("Price must be positive.")
        return price

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    subject = forms.CharField(max_length=200)
    message = forms.CharField(widget=forms.Textarea)
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if not email.endswith('@company.com'):
            raise forms.ValidationError("Must use company email.")
        return email

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
```

### Form in Views
```python
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.created_by = request.user
            product.save()
            messages.success(request, 'Product created successfully!')
            return redirect('store:product-detail', pk=product.pk)
    else:
        form = ProductForm()
    
    return render(request, 'products/form.html', {'form': form})
```

### Form in Templates
```html
<form method="post" enctype="multipart/form-data">
    {% csrf_token %}
    
    <!-- Render entire form -->
    {{ form.as_p }}
    
    <!-- Manual field rendering -->
    <div class="form-group">
        {{ form.name.label_tag }}
        {{ form.name }}
        {% if form.name.errors %}
            <div class="error">{{ form.name.errors }}</div>
        {% endif %}
    </div>
    
    <!-- Custom styling -->
    {% for field in form %}
        <div class="form-group">
            {{ field.label_tag }}
            {{ field|add_class:"form-control" }}
            {% if field.errors %}
                <div class="text-danger">{{ field.errors }}</div>
            {% endif %}
        </div>
    {% endfor %}
    
    <button type="submit">Save</button>
</form>
```

### Form Field Types
```python
# Text fields
CharField(max_length=100)
EmailField()
URLField()
SlugField()

# Numeric fields
IntegerField()
FloatField()
DecimalField(max_digits=10, decimal_places=2)

# Choice fields
CHOICES = [('option1', 'Option 1'), ('option2', 'Option 2')]
ChoiceField(choices=CHOICES)
MultipleChoiceField(choices=CHOICES)
ModelChoiceField(queryset=Category.objects.all())
ModelMultipleChoiceField(queryset=Tag.objects.all())

# Date/time fields
DateField()
TimeField()
DateTimeField()

# File fields
FileField()
ImageField()

# Boolean fields
BooleanField()
NullBooleanField()

# Custom widgets
CharField(widget=forms.Textarea)
CharField(widget=forms.PasswordInput)
DateField(widget=forms.DateInput(attrs={'type': 'date'}))
```

---

## Authentication & Authorization

### Built-in Authentication Views
```python
# urls.py
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password-change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
]

# settings.py
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
```

### User Model Extension
```python
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)

# settings.py
AUTH_USER_MODEL = 'accounts.CustomUser'

# Profile model (alternative approach)
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
```

### Permissions and Groups
```python
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

# Create group
editors = Group.objects.create(name='Editors')

# Add permissions
content_type = ContentType.objects.get_for_model(Product)
permission = Permission.objects.create(
    codename='can_publish',
    name='Can Publish Products',
    content_type=content_type,
)
editors.permissions.add(permission)

# Add user to group
user.groups.add(editors)

# Check permissions
user.has_perm('store.can_publish')
user.has_perm('store.add_product')

# In views
from django.contrib.auth.decorators import permission_required

@permission_required('store.can_publish')
def publish_product(request, pk):
    # View logic
    pass

# In templates
{% if perms.store.can_publish %}
    <a href="{% url 'publish-product' product.pk %}">Publish</a>
{% endif %}
```

### Custom Authentication
```python
# Custom authentication backend
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User

class EmailBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None
    
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

# settings.py
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'accounts.backends.EmailBackend',
]
```

---

## Static Files & Media

### Settings Configuration
```python
# settings.py
import os

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Media files (user uploads)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Static file finders
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]
```

### Directory Structure
```
myproject/
├── static/                 # Project-wide static files
│   ├── css/
│   ├── js/
│   └── images/
├── media/                  # User uploads
│   ├── uploads/
│   └── images/
├── myapp/
│   └── static/            # App-specific static files
│       └── myapp/
│           ├── css/
│           ├── js/
│           └── images/
└── staticfiles/           # Collected static files (production)
```

### Using Static Files in Templates
```html
{% load static %}

<link rel="stylesheet" type="text/css" href="{% static 'css/style.css' %}">
<script src="{% static 'js/script.js' %}"></script>
<img src="{% static 'images/logo.png' %}" alt="Logo">

<!-- With media files -->
{% if product.image %}
    <img src="{{ product.image.url }}" alt="{{ product.name }}">
{% endif %}
```

### File Upload Handling
```python
# models.py
class Product(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='products/', blank=True)
    
    def delete(self, *args, **kwargs):
        # Delete file when model is deleted
        if self.image:
            self.image.delete()
        super().delete(*args, **kwargs)

# Custom upload path
def product_image_path(instance, filename):
    return f'products/{instance.category.slug}/{filename}'

class Product(models.Model):
    image = models.ImageField(upload_to=product_image_path)
```

### Production Static Files
```bash
# Collect static files for production
python manage.py collectstatic

# With whitenoise (for Heroku)
pip install whitenoise

# settings.py
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    # ... other middleware
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

---

## Best Practices

### Project Structure
```
myproject/
├── config/                 # Project settings
│   ├── settings/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── development.py
│   │   ├── production.py
│   │   └── testing.py
│   ├── urls.py
│   └── wsgi.py
├── apps/                   # Django apps
│   ├── accounts/
│   ├── store/
│   └── api/
├── static/
├── media/
├── templates/
├── requirements/
│   ├── base.txt
│   ├── development.txt
│   └── production.txt
└── manage.py
```

### Settings Management
```python
# base.py
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Common settings
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    # ... other apps
    'apps.accounts',
    'apps.store',
]

# development.py
from .base import *

DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# production.py
from .base import *
import dj_database_url

DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com']

DATABASES = {
    'default': dj_database_url.parse(os.environ.get('DATABASE_URL'))
}
```

### Security Best Practices
```python
# settings.py
# Security settings
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# HTTPS in production
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Environment variables
import os
from decouple import config

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
DATABASE_URL = config('DATABASE_URL')
```

### Code Organization
```python
# Fat models, thin views
class Product(models.Model):
    # ... fields
    
    @property
    def is_available(self):
        return self.inventory > 0 and self.is_active
    
    def reduce_inventory(self, quantity):
        if self.inventory >= quantity:
            self.inventory -= quantity
            self.save()
            return True
        return False
    
    @classmethod
    def get_featured(cls):
        return cls.objects.filter(is_featured=True, is_active=True)

# Managers for common queries
class ProductManager(models.Manager):
    def available(self):
        return self.filter(inventory__gt=0, is_active=True)
    
    def by_category(self, category):
        return self.filter(category=category)

class Product(models.Model):
    objects = ProductManager()
    # ... fields and methods
```

### Testing
```python
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Product, Category

class ProductModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Electronics')
        self.product = Product.objects.create(
            name='Smartphone',
            price=999.99,
            category=self.category
        )
    
    def test_string_representation(self):
        self.assertEqual(str(self.product), 'Smartphone')
    
    def test_get_absolute_url(self):
        self.assertEqual(self.product.get_absolute_url(), f'/products/{self.product.id}/')

class ProductViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('testuser', 'test@example.com', 'pass')
        self.category = Category.objects.create(name='Electronics')
        self.product = Product.objects.create(
            name='Smartphone',
            price=999.99,
            category=self.category
        )
    
    def test_product_list_view(self):
        response = self.client.get(reverse('store:product-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Smartphone')
    
    def test_product_create_requires_login(self):
        response = self.client.get(reverse('store:product-create'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_product_create_with_login(self):
        self.client.login(username='testuser', password='pass')
        response = self.client.post(reverse('store:product-create'), {
            'name': 'New Product',
            'price': '199.99',
            'category': self.category.id,
        })
        self.assertEqual(response.status_code, 302)  # Redirect after creation
        self.assertTrue(Product.objects.filter(name='New Product').exists())
```

### Performance Optimization
```python
# Use select_related for foreign keys
products = Product.objects.select_related('category').all()

# Use prefetch_related for reverse foreign keys and many-to-many
categories = Category.objects.prefetch_related('product_set').all()

# Use only() to limit fields
products = Product.objects.only('name', 'price').all()

# Use defer() to exclude fields
products = Product.objects.defer('description').all()

# Database indexing
class Product(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['category', 'price']),
            models.Index(fields=['name', 'is_active']),
        ]

# Caching
from django.core.cache import cache
from django.views.decorators.cache import cache_page

@cache_page(60 * 15)  # Cache for 15 minutes
def product_list(request):
    # ... view logic

# Template fragment caching
{% load cache %}
{% cache 500 product_list %}
    <!-- expensive template code -->
{% endcache %}
```

### Environment Management
```bash
# requirements/base.txt
Django>=4.2,<5.0
Pillow>=10.0.0
python-decouple>=3.8

# requirements/development.txt
-r base.txt
django-debug-toolbar>=4.2.0
django-extensions>=3.2.3

# requirements/production.txt
-r base.txt
gunicorn>=21.2.0
psycopg2-binary>=2.9.7
whitenoise>=6.5.0

# .env file
SECRET_KEY=your-secret-key-here
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
```

---

## Quick Commands Cheat Sheet

```bash
# Project setup
django-admin startproject myproject
cd myproject
python manage.py startapp myapp

# Database
python manage.py makemigrations
python manage.py migrate
python manage.py dbshell

# User management
python manage.py createsuperuser
python manage.py changepassword username

# Development server
python manage.py runserver
python manage.py runserver 8080
python manage.py runserver 0.0.0.0:8000

# Static files
python manage.py collectstatic
python manage.py findstatic css/style.css

# Shell
python manage.py shell
python manage.py shell_plus  # with django-extensions

# Testing
python manage.py test
python manage.py test myapp
python manage.py test myapp.tests.ProductTestCase

# Other useful commands
python manage.py check
python manage.py showmigrations
python manage.py sqlmigrate myapp 0001
python manage.py dumpdata > backup.json
python manage.py loaddata backup.json
```

---

## Useful Packages

### Development
- **django-debug-toolbar**: Debug information panel
- **django-extensions**: Additional management commands
- **django-environ**: Environment variable management
- **ipython**: Enhanced Python shell

### Production
- **gunicorn**: WSGI HTTP Server
- **whitenoise**: Static file serving
- **psycopg2-binary**: PostgreSQL adapter
- **redis**: Caching and session storage

### Forms & UI
- **django-crispy-forms**: Better form rendering
- **django-widget-tweaks**: Form field customization
- **django-bootstrap4**: Bootstrap integration

### API Development
- **djangorestframework**: REST API framework
- **django-cors-headers**: CORS handling
- **django-filter**: Advanced filtering

### Authentication
- **django-allauth**: Social authentication
- **djangorestframework-simplejwt**: JWT authentication
- **django-oauth-toolkit**: OAuth2 provider

---

This cheat sheet covers the fundamental Django concepts and patterns. Keep it handy for quick reference during development! 🚀
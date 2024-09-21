from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator
import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save
#from .models import Product, Customer

#create customer profile
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_modified = models.DateTimeField(User, auto_now=True)
    phone = models.CharField(max_length=20, blank=True)
    address1 =  models.CharField(max_length=200, blank=True)
    address2 =  models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=50, blank=True)
    state = models.CharField(max_length=50, blank=True)
    zipcode = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=20, blank=True)
    old_cart = models.CharField(max_length=200, blank=True, null=True)
    
    def __str__(self):
        return self.user.username
    
#create a user Profile by default when user signs up
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()
#Automate the profile thing
post_save.connect(create_profile, sender=User)            


class Category(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Customer(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone = models.CharField(max_length=20)
    business_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    address = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    date = models.DateField(default=datetime.datetime.today())

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class Product(models.Model):
    name = models.CharField(max_length=40)
    description = models.CharField(max_length=500, default='', blank=True, null=True)
    price = models.DecimalField(default=0, decimal_places=2, max_digits=8)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    picture = models.ImageField(upload_to='upload/product/') 
    star = models.IntegerField(default=0, validators=[MaxValueValidator(5),MinValueValidator(0)])
    date = models.DateField(default=datetime.datetime.today())

    is_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(default=0, decimal_places=2, max_digits=5)
    
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.ImageField(default=1)
    address = models.CharField(max_length=400, default='', blank=True)
    phone = models.CharField(max_length=20, blank=True)
    date = models.DateField(default=datetime.datetime.today())
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.product   

# class Inventory(models.Model):
#     product = models.OneToOneField('Product', on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField(default=0)

#     def __str__(self):
#         return f"{self.product.name} - {self.quantity} item in stock"
    
class Invoice(models.Model):
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    products = models.ManyToManyField('Product', through='InvoiceProduct')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Invoice {self.id} for {self.customer.first_name} {self.customer.last_name}"

class InvoiceProduct(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} - {self.quantity} pcs"         
    
class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/')
    #alt_text = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Image for {self.product.name}"

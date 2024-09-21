from django.db import models
from django.contrib.auth.models import User
from shop.models import Product
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
import datetime
#from payment.models import Order, OrderItem


class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    shipping_full_name = models.CharField(max_length=255)
    shipping_email = models.CharField(max_length=255)
    shipping_address1 = models.CharField(max_length=255)
    shipping_address2 = models.CharField(max_length=255, null=True, blank=True)
    shipping_city = models.CharField(max_length=255)
    shipping_state = models.CharField(max_length=255, null=True, blank=True)
    shipping_zipcode = models.CharField(max_length=255,null=True, blank=True)
    shipping_country = models.CharField(max_length=255)
    

    class Meta:
        verbose_name_plural = "Shipping Address"

    def __str__(self):
        return f'Shipping Address - {str(self.id)}'   

#create a user Shipping Address by default when user signs up
def create_shipping(sender, instance, created, **kwargs):
    if created:
        user_shipping = ShippingAddress(user=instance)
        user_shipping.save()
#Automate the profile thing
post_save.connect(create_shipping, sender=User)            


# Create Order Model
class Order(models.Model):
    # Foreign key
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=250)
    email = models.EmailField(max_length=250)
    shipping_address = models.TextField(max_length=15000)
    amount_paid = models.DecimalField(max_digits=8, decimal_places=2)
    date_ordered = models.DateTimeField(auto_now_add=True)
    shipped = models.BooleanField(default=False)
    date_shipped = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f'Order - {str(self.id)}'
# Auto add shipping date
@receiver(pre_save, sender=Order)
def set_shipped_date_on_update(sender, instance, **kwargs):
    if instance.pk:
        now = datetime.datetime.now()
        obj = sender._default_manager.get(pk=instance.pk)
        if instance.shipped and not obj.shipped:
            instance.date_shipped = now

# Create Order Items Model     
class OrderItem(models.Model):
    # Foreign keys
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
  
    quantity = models.PositiveBigIntegerField(default=1)
    stock = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=8, decimal_places=2)


    def __str__(self):
        return f'Order Item - {str(self.id)}'
    


#Create invoice and reduce stock
# class Invoice(models.Model):
#     invoice_number = models.CharField(max_length=20, unique=True)
#     order = models.OneToOneField(Order, on_delete=models.CASCADE)
#     customer_name = models.CharField(max_length=255)
#     customer_phone = models.CharField(max_length=20)
#     customer_address = models.TextField()
#     date = models.DateTimeField(auto_now_add=True)
#     total_amount = models.DecimalField(max_digits=10, decimal_places=2)

#     def __str__(self):
#         return f'Invoice {self.invoice_number} for Order {self.order.id}'

#     def save(self, *args, **kwargs):
#         if not self.invoice_number:
#             self.invoice_number = self.generate_invoice_number()
#         super().save(*args, **kwargs)

#     def generate_invoice_number(self):
#         last_invoice = Invoice.objects.all().order_by('id').last()
#         if not last_invoice:
#             return 'INV0001'
#         invoice_number = last_invoice.invoice_number
#         invoice_int = int(invoice_number.split('INV')[-1])
#         new_invoice_int = invoice_int + 1
#         new_invoice_number = 'INV' + str(new_invoice_int).zfill(4)
#         return new_invoice_number

# class InvoiceItem(models.Model):
#     invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='items')
#     product_name = models.CharField(max_length=255)
#     quantity = models.PositiveIntegerField()
#     price = models.DecimalField(max_digits=10, decimal_places=2)

#     def __str__(self):
#         return f'{self.quantity} x {self.product_name}'

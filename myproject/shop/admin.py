from django.contrib import admin
from . import models
from django.contrib.auth.models import User
from .models import Category, Customer, Product, Order, Profile, Invoice, InvoiceProduct, ProductImage


admin.site.register(models.Category)
admin.site.register(models.Customer)
#admin.site.register(models.Product)
admin.site.register(models.Order)
admin.site.register(models.Profile)
#admin.site.register(models.Inventory)
admin.site.register(models.Invoice)
admin.site.register(models.InvoiceProduct)


# Mix profile info and user info
class ProfileInline(admin.StackedInline):
    model = Profile 

class UserAdmin(admin.ModelAdmin):
    model = User   
    field = ["username", "first_name", "last_name", "email"]
    inlines = [ProfileInline]

# unregister the old way
admin.site.unregister(User)

# Re-Register the new way
admin.site.register(User, UserAdmin)

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price','stock','category')
    inlines = [ProductImageInline]

admin.site.register(Product, ProductAdmin)    
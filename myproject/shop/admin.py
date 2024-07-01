from django.contrib import admin
from . import models
from django.contrib.auth.models import User
from .models import Category, Customer, Product, Order, Profile


admin.site.register(models.Category)
admin.site.register(models.Customer)
admin.site.register(models.Product)
admin.site.register(models.Order)
admin.site.register(models.Profile)


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
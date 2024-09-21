from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Category, Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoFom
#from django.db import transaction
#from django.http import HttpResponseBadRequest

from payment.forms import ShippingForm
from payment.models import ShippingAddress

from django.db.models import Q
import json
from cart.cart import Cart

def helloworld(request):
    all_products = Product.objects.all()

    return render(request, 'index.html', {'products': all_products})

def about(request):
    return render(request, 'about.html')

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request,username=username, password=password)
        if user is not None:
            login(request, user)

            # Do some shopping cart stuff
            current_user = Profile.objects.get(user__id=request.user.id)
            # Get their save cart from database
            saved_cart = current_user.old_cart 
            # Convert database string to python dictionary
            if saved_cart:
                # Convert to dictionary using JSON
                converted_cart = json.loads(saved_cart)     
                # Add the loaded cart dictionary to our session 
                # Get the cart
                cart = Cart(request)
                # Loop thro the cart and add the items from the database
                for key,value in converted_cart.items():
                    cart.db_add(product=key, quantity=value)



            messages.success(request,("You have successfully logged in!"))
            return redirect("home")
        else:
            messages.success(request,("There is a problem in login!"))
            return redirect("login")
    else:    
        return render(request, 'login.html')

def logout_user(request):
    logout(request)
    messages.success(request, ("You have successfully logged out!"))
    return redirect("home")

def signup_user(request):
    
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            if user is not None:
               login(request, user)
               messages.success(request,('Username created -Please fill out your user info below...!'))
               return redirect("update_info")
            else:
               messages.error(request,('There was a problem logging you in after registration!'))
               return redirect("signup")
        else:
            messages.error(request,'There is a problem with your registration!')
            print(form.errors)         
    else:   
        form = SignUpForm()
    return render(request, 'signup.html', {'form':form})

def update_info(request):
    if request.method == "POST":
        form = UserInfoFom(request.POST)
    if request.user.is_authenticated:
        # Get current user
        current_user = Profile.objects.get(user__id=request.user.id)
        # Get current user's shipping info
        Shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        
        # Get original User form
        form = UserInfoFom(request.POST or None, instance=current_user)
        # Get user's shipping form
        shipping_form = ShippingForm(request.POST or None, instance=Shipping_user)    

        if form.is_valid() or shipping_form.is_valid():
            # Save original form
            form.save()
            # Save shipping form
            shipping_form.save()

            messages.success(request, "Your info has been updated!")
            return redirect('home')
        return render(request, 'update_info.html',{'form':form, 'shipping_form':shipping_form})
    else:
        messages.success(request, "You must be logged in to access the page!")
        return redirect('home')

def update_password(request):
    if request.method == "POST":
        form =ChangePasswordForm(request.POST)
    if request.user.is_authenticated:
        current_user = request.user
        #Did they fill out the  form
        if request.method == 'POST':
            form = ChangePasswordForm(current_user, request.POST)
            #Is the form valid
            if form.is_valid():
                form.save()
                messages.success(request, "Your Password has been updated!")
                login(request, current_user)
                return redirect('update_user')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                    return redirect('update_password')

        else:
            form = ChangePasswordForm(current_user)    
            return render(request, 'update_password.html',{'form':form})
    else:
         messages.success(request, "You must be logged in to view that page...!")
         return redirect('home')

def update_user(request):
    if request.method == "POST":
        form = UpdateUserForm(request.POST)
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_user)

        if user_form.is_valid():
            user_form.save()

            login(request, current_user)
            messages.success(request, "User has been updated!")
            return redirect('home')
        return render(request, 'update_user.html',{'user_form':user_form})
    else:
        messages.success(request, "You must be logged in to access the page!")
        return redirect('home')
 

def product(request,pk):
    product = Product.objects.get(id=pk)
   # images = product.images.all()
    return render(request, 'product.html', {'product': product})

def search(request):
    # Determine if they filled out the form
    if request.method == "POST":
        searched = request.POST['searched']
        # Query the Products DB Model
        searched = Product.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched)) 
        # Test for null
        if not searched:
            messages.success(request, "That Product does not exist..Please try again.")
            return render(request, 'search.html', {})
        else:
            return render(request, 'search.html',{'searched':searched})
    else: 
        return render(request, 'search.html',{})




def category_summary(request):
    categories = Category.objects.all()
    return render(request, 'category_summary.html', {'categories':categories})

def category(request,cat):
    cat = cat.replace("-"," ")
    try:
        category = Category.objects.get(name=cat)
        products = Product.objects.filter(category=category)
        return render(request, 'category.html', {'products': products, "category":category})
    except:
        messages.error(request, ('There is no category!'))
        return redirect("home")
       



def product_image(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    images = product.images.all()  #Retrieve all images for this product

    return render(request, 'product.html', {'product': product, 'images': images})

def invoice_success(request):
    return render(request, 'invoice_success.html')

def create_invoice():
    pass
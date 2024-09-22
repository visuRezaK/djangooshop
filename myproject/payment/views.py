from django.shortcuts import render, redirect
from cart.cart import Cart
from payment.forms import ShippingForm, PaymentForm
from payment.models import ShippingAddress, Order, OrderItem
from django.contrib import messages
from django.contrib.auth.models import User 
from shop.models import Customer, Product, Profile
import datetime
# Import Some Paypal Stuff 
from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
import uuid # unique user id for duplicate orders


def orders(request, pk):
     if request.user.is_authenticated and request.user.is_superuser:
         # Get the order
         order = Order.objects.get(id=pk)
         # Get the order items
         items = OrderItem.objects.filter(order=pk)

         if request.POST:
             status = request.POST['shipping_status']
             # Check if true or false
             if status == "true":
                 # Get the order
                 order = Order.objects.filter(id=pk)
                 # Update the status
                 now = datetime.datetime.now()
                 order.update(shipped=True, date_shipped=now)
             else:
                  # Get the order
                 order = Order.objects.filter(id=pk)
                 # Update the status
                 order.update(shipped=False)
             messages.success(request, "Shipping Status Updated")  
             return redirect('home')   
                      

         return render(request, 'payment/orders.html', {"order":order, "items":items})
     else:
      messages.success(request, "Access Denied!")
      return redirect('home')   



def not_shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
       orders = Order.objects.filter(shipped=False)
       if request.POST:
           status = request.POST['shipping_status']
           num = request.POST['num']
           # Get the order
           order = Order.objects.filter(id=num)

           # Grab Date and Time
           now = datetime.datetime.now()
           
           # Update  order             
           order.update(shipped=True, date_shipped=now)
           # Redirect
           messages.success(request, "Shipping Status Updated")  
           return redirect('home')   

       return render(request, "payment/not_shipped_dash.html", {"orders":orders})
    else:
        messages.success(request, "Access Denied!")
        return redirect('home')

def shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped=True)
        if request.POST:
           status = request.POST['shipping_status']
           num = request.POST['num']
           # Grab the order
           order = Order.objects.filter(id=num)
           # Grab Date and Time
           now = datetime.datetime.now()
           
           # Update  order             
           order.update(shipped=False)
           # Redirect
           messages.success(request, "Shipping Status Updated")  
           return redirect('home')   




        return render(request, "payment/shipped_dash.html", {"orders":orders})
    else:
        messages.success(request, "Access Denied!")
        return redirect('home')


def process_order(request):
    if request.POST:
       # Get the cart
       cart = Cart(request)
       cart_products = cart.get_prods()
       quantities = cart.get_quants()
       totals = cart.cart_total()
       
       # Get Billing info from the last page
       payment_form = PaymentForm(request.POST or None)
       # Get Shipping session data 
       my_shipping = request.session.get('my_shipping')

       # Get Order info 
       full_name =  my_shipping['shipping_full_name']
       email =  my_shipping["shipping_email"]
      # Create shipping Address from session info
       shipping_address = f"{my_shipping['shipping_address1']}\n{my_shipping['shipping_address2']}\n{my_shipping['shipping_city']}\n{my_shipping['shipping_state']}\n{my_shipping['shipping_zipcode']}\n{my_shipping['shipping_country']}"
       amount_paid = totals

       # Create an Order
       if request.user.is_authenticated:
           # logged in
           user = request.user 
           # Create Order
           create_order = Order(user=user, full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid)
           create_order.save()


           # Add order items
           # Get the order ID
           order_id = create_order.pk

           # Get product Info
           for product in cart_products:
               # Get product Id
               product_id = product.id
               # Get product price
               if product.is_sale:
                   price = product.sale_price
               else:
                   price = product.price

                # Get quantity
               for key, value in quantities.items():
                   if int(key) == product.id:
                       # Create order item
                       create_order_item = OrderItem(order_id=order_id, product_id=product_id, user=user, quantity=value, price=price)
                       create_order_item.save()   
                       # Reduce stock
                       product.stock -= value
                       product.save()  
            # Delete our cart
           for key in list(request.session.keys()):
                if key == "session_key":
                    # Delete the key
                    del request.session[key]

            # Delete Cart from Database (old_cart field)
           current_user = Profile.objects.filter(user__id=request.user.id)
            # Delete shopping cart in database (old_cart field)
           current_user.update(old_cart="")       
             
           messages.success(request, "Order Placed!")
           return redirect('home')  
       else:
           # not logged in
           # Create Order
           create_order = Order(full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid)
           create_order.save() 
           # Add order items
           # Get the order ID
           order_id = create_order.pk

           # Get product Info
           for product in cart_products:
               # Get product Id
               product_id = product.id
               # Get product price
               if product.is_sale:
                   price = product.sale_price
               else:
                   price = product.price

                # Get quantity
               for key,value in quantities.items():
                   if int(key) == product.id:
                       # Create order item
                       create_order_item = OrderItem(order_id=order_id, product_id=product_id, quantity=value, price=price)
                       create_order_item.save()   
                       product.stock -= value
                       product.save()  
            # Delete our cart
           for key in list(request.session.keys()):
                if key == "session_key":
                    # Delete the key
                    del request.session[key]
             
            
                        
           messages.success(request, "Order Placed!")
           return redirect('home')  

    else:
        messages.success(request, "Access Denied")
        return redirect('home')   


def billing_info(request):
    if request.POST:
        # Get the cart
        cart = Cart(request)
        cart_products = cart.get_prods()
        quantities = cart.get_quants()
        totals = cart.cart_total()

        # Create a session with Shipping info
        my_shipping = request.POST
        request.session['my_shipping'] = my_shipping

        # Get the host
        host = request.get_host()
        # Create Paypal Form Dictionary
        paypal_dict ={
            'business': settings.PAYPAL_RECEIVER_EMAIL,
            'amount': totals,
            'item_name':'Computer Order',
            'no_shipping': '2',
            'invoice': str(uuid.uuid4()),
            'currency_code': 'USD',
            'notify_url':'https://{}{}'.format(host, reverse("paypal-ipn")),
            'return_url':'https://{}{}'.format(host, reverse("payment_success")),
            'cancel_return':'https://{}{}'.format(host, reverse("payment_failed")),
        }

        # Create actual paypal button
        paypal_form = PayPalPaymentsForm(initial=paypal_dict)


        # Check to see if user is logged in 
        if request.user.is_authenticated:
            # Get the Billing form
            billing_form = PaymentForm()
            return render(request, "payment/billing_info.html", {'paypal_form':paypal_form, 'cart_products':cart_products, 'quantities':quantities, 'totals':totals, 'shipping_info':request.POST, 'billing_form':billing_form})
        else:
            # Not logged in 
            # Get the Billing form
            billing_form = PaymentForm()
            return render(request, "payment/billing_info.html", {'paypal_form':paypal_form,'cart_products':cart_products, 'quantities':quantities, 'totals':totals, 'shipping_info':request.POST, 'billing_form':billing_form})


        shipping_form = request.POST
        return render(request, "payment/billing_info.html", {'cart_products':cart_products, 'quantities':quantities, 'totals':totals, 'shipping_form':shipping_form})
    else:
        messages.success(request, "Access Denied")
        return redirect('home')


def checkout(request):
    # Get the cart
    cart = Cart(request)
    cart_products = cart.get_prods()
    quantities = cart.get_quants()
    totals = cart.cart_total()
    # Check if stock is sufficient for each product
    # for product in cart_products:
    #      quantity = quantities.get(str(product.id))
    #      if product.stock < quantity or product.stock <= 0:
    #          messages.error(request, f'The stock is not enough for {product.name}, please try another time.')
    #          return redirect('home')  # Redirect to the cart page or wherever you want

    error_messages = []        

    if request.user.is_authenticated:
        # Checkout as logged user
        # Shipping User
        for product in cart_products:
          quantity = quantities.get(str(product.id))
          if product.stock < quantity or product.stock <= 0:
              error_messages.append(f'The stock is not enough for {product.name}, please try another time.')
        if error_messages:
            for msg in error_messages:
                    messages.error(request, msg)
            return redirect('home')  # Redirect to the appropriate page, e.g., the cart page

              #messages.error(request, f'The stock is not enough for {product.name}, please try another time.')
              #return redirect('home')  # Redirect to the cart page or wherever you want
          
        Shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        # Shipping Form
        shipping_form = ShippingForm(request.POST or None, instance=Shipping_user) 
        return render(request, "payment/checkout.html", {'cart_products':cart_products, 'quantities':quantities, 'totals':totals, 'shipping_form':shipping_form})
    else:
       for product in cart_products:
          quantity = quantities.get(str(product.id))
          if product.stock < quantity or product.stock <= 0:
              error_messages.append(f'The stock is not enough for {product.name}, please try another time.')
       if error_messages:
            for msg in error_messages:
                    messages.error(request, msg)
            return redirect('home')  # Redirect to the appropriate page, e.g., the cart page
       # Checkout as guest
       shipping_form = ShippingForm(request.POST or None) 
       return render(request, "payment/checkout.html", {'cart_products':cart_products, 'quantities':quantities, 'totals':totals, 'shipping_form':shipping_form})

    
def payment_success(request):
    return render(request, "payment/payment_success.html", {})

def payment_failed(request):
    return render(request, "payment/payment_failed.html")









# from gettext import translation
# #from inspect import stock
# from django.http import HttpResponseBadRequest
# from django.shortcuts import get_object_or_404, render, redirect
# from cart.cart import Cart
# from payment.forms import ShippingForm, PaymentForm
# from payment.models import Invoice, InvoiceItem, ShippingAddress, Order, OrderItem
# from django.contrib import messages
# from django.contrib.auth.models import User
# from shop.models import Customer, InvoiceProduct, Product, Profile, Order
# import datetime




# def orders(request, pk):
#      if request.user.is_authenticated and request.user.is_superuser:
#          # Get the order
#          order = Order.objects.get(id=pk)
#          # Get the order items
#          items = OrderItem.objects.filter(order=pk)

#          if request.POST:
#              status = request.POST['shipping_status']
#              # Check if true or false
#              if status == "true":
#                  # Get the order
#                  order = Order.objects.filter(id=pk)
#                  # Update the status
#                  now = datetime.datetime.now()
#                  order.update(shipped=True, date_shipped=now)
#              else:
#                   # Get the order
#                  order = Order.objects.filter(id=pk)
#                  # Update the status
#                  order.update(shipped=False)
#              messages.success(request, "Shipping Status Updated")  
#              return redirect('home')   
                      

#          return render(request, 'payment/orders.html', {"order":order, "items":items})
#      else:
#       messages.success(request, "Access Denied!")
#       return redirect('home')   



# def not_shipped_dash(request):
#     if request.user.is_authenticated and request.user.is_superuser:
#        orders = Order.objects.filter(shipped=False)
#        if request.POST:
#            status = request.POST['shipping_status']
#            num = request.POST['num']
#            # Get the order
#            order = Order.objects.filter(id=num)

#            # Grab Date and Time
#            now = datetime.datetime.now()
           
#            # Update  order             
#            order.update(shipped=True, date_shipped=now)
#            # Redirect
#            messages.success(request, "Shipping Status Updated")  
#            return redirect('home')   

#        return render(request, "payment/not_shipped_dash.html", {"orders":orders})
#     else:
#         messages.success(request, "Access Denied!")
#         return redirect('home')

# def shipped_dash(request):
#     if request.user.is_authenticated and request.user.is_superuser:
#         orders = Order.objects.filter(shipped=True)
#         if request.POST:
#            status = request.POST['shipping_status']
#            num = request.POST['num']
#            # Grab the order
#            order = Order.objects.filter(id=num)
#            # Grab Date and Time
#            now = datetime.datetime.now()
           
#            # Update  order             
#            order.update(shipped=False)
#            # Redirect
#            messages.success(request, "Shipping Status Updated")  
#            return redirect('home')   




#         return render(request, "payment/shipped_dash.html", {"orders":orders})
#     else:
#         messages.success(request, "Access Denied!")
#         return redirect('home')


# def process_order(request):
#     if request.POST:
#        # Get the cart
#        cart = Cart(request)
#        cart_products = cart.get_prods()
#        quantities = cart.get_quants()
#        totals = cart.cart_total()
       
#        # Get Billing info from the last page
#        payment_form = PaymentForm(request.POST or None)
#        # Get Shipping session data 
#        my_shipping = request.session.get('my_shipping')

#        # Get Order info 
#        full_name =  my_shipping['shipping_full_name']
#        email =  my_shipping["shipping_email"]
#       # Create shipping Address from session info
#        shipping_address = f"{my_shipping['shipping_address1']}\n{my_shipping['shipping_address2']}\n{my_shipping['shipping_city']}\n{my_shipping['shipping_state']}\n{my_shipping['shipping_zipcode']}\n{my_shipping['shipping_country']}"
#        amount_paid = totals

#        # Create an Order
#        if request.user.is_authenticated:
#            # logged in
#            user = request.user          
#            # Create Order
#            create_order = Order(user=user, full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid)
#            create_order.save()


#            # Add order items
#            # Get the order ID
#            order_id = create_order.pk

#            # Get product Info
#            for product in cart_products:
#                # Get product Id
#                product_id = product.id
#                # Get product price
#                if product.is_sale:
#                    price = product.sale_price
#                else:
#                    price = product.price

#                 # Get quantity
#                for key, value in quantities.items():
#                    if int(key) == product.id:
#                        # Create order item
#                        create_order_item = OrderItem(order_id=order_id, product_id=product_id, user=user, quantity=value, price=price, stock=value)
#                        create_order_item.save()   
#                        # Reduce stock
#                        product.stock -= value
#                        product.save() 
#             # Delete our cart
#            for key in list(request.session.keys()):
#                 if key == "session_key":
#                     # Delete the key
#                     del request.session[key]

#             # Delete Cart from Database (old_cart field)
#            current_user = Profile.objects.filter(user__id=request.user.id)
#             # Delete shopping cart in database (old_cart field)
#            current_user.update(old_cart="")       
             
#            messages.success(request, "Order Placed!")
#            return redirect('home')  
#        else:
#            # not logged in
#            # Create Order
#            create_order = Order(full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid)
#            create_order.save() 
#            # Add order items
#            # Get the order ID
#            order_id = create_order.pk

#            # Get product Info
#            for product in cart_products:
#                # Get product Id
#                product_id = product.id
#                # Get product price
#                if product.is_sale:
#                    price = product.sale_price
#                else:
#                    price = product.price

#                 # Get quantity
#                for key,value in quantities.items():
#                    if int(key) == product.id:
#                        # Create order item
#                        create_order_item = OrderItem(order_id=order_id, product_id=product_id, quantity=value, price=price, stock=value)
#                        create_order_item.save()   
                    
#                        # Reduce stock
#                        product.stock -= value
#                        product.save() 

#             # Delete our cart
#            for key in list(request.session.keys()):
#                 if key == "session_key":
#                     # Delete the key
#                     del request.session[key]
             
            
                        
#            messages.success(request, "Order Placed!")
#            return redirect('home')  

#     else:
#         messages.success(request, "Access Denied")
#         return redirect('home')   



# def billing_info(request):
#     if request.POST:
#         # Get the cart
#         cart = Cart(request)
#         cart_products = cart.get_prods()
#         quantities = cart.get_quants()
#         totals = cart.cart_total()

#         # Create a session with Shipping info
#         my_shipping = request.POST
#         request.session['my_shipping'] = my_shipping

#         # Check to see if user is logged in 
#         if request.user.is_authenticated:
#             # Get the Billing form
#             billing_form = PaymentForm()
#             return render(request, "payment/billing_info.html", {'cart_products':cart_products, 'quantities':quantities, 'totals':totals, 'shipping_info':request.POST, 'billing_form':billing_form})
#         else:
#             # Not logged in 
#             # Get the Billing form
#             billing_form = PaymentForm()
#             return render(request, "payment/billing_info.html", {'cart_products':cart_products, 'quantities':quantities, 'totals':totals, 'shipping_info':request.POST, 'billing_form':billing_form})


#         shipping_form = request.POST
#         return render(request, "payment/billing_info.html", {'cart_products':cart_products, 'quantities':quantities, 'totals':totals, 'shipping_form':shipping_form})
#     else:
#         messages.success(request, "Access Denied")
#         return redirect('home')


# def checkout(request):
#     # Get the cart
#     cart = Cart(request)
#     cart_products = cart.get_prods()
#     quantities = cart.get_quants()
#     totals = cart.cart_total()

#     # Check if stock is sufficient for each product
#     for product in cart_products:
#         quantity = quantities.get(str(product.id))
#         if product.stock < quantity or product.stock <= 0:
#             messages.error(request, f'The stock is not enough for {product.name}, please try again.')
#             return redirect('home')  # Redirect to the cart page or wherever you want
            
    

#     if request.user.is_authenticated:
#         # Checkout as logged user
#         # Shipping User
#         Shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
#         # Shipping Form
#         shipping_form = ShippingForm(request.POST or None, instance=Shipping_user) 
#         return render(request, "payment/checkout.html", {'cart_products':cart_products, 'quantities':quantities, 'totals':totals, 'shipping_form':shipping_form})
#     else:
#        # Checkout as guest
#        shipping_form = ShippingForm(request.POST or None) 
#        return render(request, "payment/checkout.html", {'cart_products':cart_products, 'quantities':quantities, 'totals':totals, 'shipping_form':shipping_form})


# def payment_success(request):
#     return render(request, "payment/payment_success.html", {})


# #Payment Success
# def payment_success(request):
#     order_id = request.session.get('order_id')
#     if order_id:
#         order = Order.objects.get(id=order_id)

#         # Extract customer information from the order
#         customer_name = order.full_name
#         customer_phone = "Customer's phone number"  # Adjust as necessary
#         customer_address = order.shipping_address
#         total_amount = order.amount_paid

#         # Generate the invoice
#         invoice = Invoice(
#             order=order,
#             customer_name=customer_name,
#             customer_phone=customer_phone,
#             customer_address=customer_address,
#             total_amount=total_amount
#         )
#         invoice.save()

#         # Add items to the invoice
#         order_items = OrderItem.objects.filter(order=order)
#         for item in order_items:
#             InvoiceItem.objects.create(
#                 invoice=invoice,
#                 product_name=item.product.name,  # Product name
#                 quantity=item.quantity,          # Quantity of product
#                 price=item.price                 # Price per unit
#             )

#         # Reduce stock after invoice generation
#         for item in order_items:
#             product = item.product
#             product.stock -= item.quantity
#             product.save()

#         # Clear session
#         del request.session['order_id']

#     return render(request, "payment/payment_success.html", {'order': order})





# def create_invoice(request):
#     if request.method == 'POST':
#         customer = get_object_or_404(Customer, pk=request.POST.get('customer_id'))
#         products = request.POST.getlist('products')
#         quantities = request.POST.getlist('quantities')

#         if len(products) !=len(quantities):
#             return HttpResponseBadRequest("Invalid input: Mismatched products and quantities")
        
#         total = 0 

#         with translation.atomic():
#             invoice = Invoice.objects.create(customer=customer, total_amount=0)

#             for product_id, quantity in zip(products, quantities):
#                 product = get_object_or_404(Product, pk=product_id)
#                 quantity = int(quantity)

#                 #Check if enough stock is available:
#                 inventory = get_object_or_404(Inventory, product=product)
#                 if inventory.quantity < quantity:
#                     return HttpResponseBadRequest(f"Not enough stock for {product.name}")
                    
#                 price = product.price * quantity
#                 total += price

#                 #Create InvoiceProduct Entry\
#                 InvoiceProduct.objects.create(invoice=invoice, product=product, quantity=quantity, price=price)

#                 #Reduce Inventory Stock 
#                 #inventory.quantity -= quantity
#                 #inventory.save()

#             invoice.total_amount = total
#             invoice.save()

#         return render(request, 'invoice_success.html', {'invoice': invoice})
    
#     customers = Customer.objects.all()
#     products = Product.objects.all()
#     return render(request, 'create_invoice.html', {'customers': customers, 'products': products})


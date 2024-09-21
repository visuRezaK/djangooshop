from django.shortcuts import redirect, render, get_object_or_404

#from myproject.payment.forms import ShippingForm
#from myproject.payment.models import ShippingAddress
from .cart import Cart
from shop.models import Product
from django.http import JsonResponse
from django.contrib import messages

def cart_summary(request):
    cart = Cart(request)
    cart_products = cart.get_prods()
    quantities = cart.get_quants()
    totals = cart.cart_total()
    return render(request, "cart_summary.html", {'cart_products':cart_products, 'quantities':quantities, 'totals':totals})

def cart_add(request):
    cart = Cart(request)

    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        product = get_object_or_404(Product, id=product_id)
        cart.add(product = product, quantity = product_qty)

        cart_quantity = cart.__len__()
        
        #response = JsonResponse({'Product name' : product.name})
        response = JsonResponse({'qty' : cart_quantity})
        messages.success(request, ("Product Added to Cart..."))
        return response

def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
       product_id = int(request.POST.get('product_id'))
       #call delete Function in cart
       cart.delete(product=product_id)

       response = JsonResponse({'product':product_id})
       messages.success(request, ("Item Deleted From Shopping Cart..."))
       return response
    

def cart_update(request):
    
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_qty =request.POST.get('product_qty')
        if product_qty:
            product_qty = int(product_qty)


            cart.update(product=product_id, quantity=product_qty)

            response = JsonResponse({'qty':product_qty})
            messages.success(request, ("Your Cart Has Been Updated..."))
            return response
        else:
            return JsonResponse({'error': 'product not '}, status=400)
        

# def check_stock(request):
#     cart = Cart(request)
#     # Get the product ID and quantity from the request
#     product_id = request.GET.get('product_id')
#     quantity = int(request.GET.get('quantity'))
#     if request.POST.get('action') == 'post':
#         # What do you want to do when the action is 'post'?
#         # You might want to update the cart or perform some other action
#         pass
#     # Check the stock quantity for the product
#     product = Product.objects.get(id=product_id)
#     if product.stock_quantity <= 0 or product.stock_quantity < quantity:
#         return JsonResponse({'available': False})
#     else:
#         return JsonResponse({'available': True})


from django.shortcuts import render, redirect,get_object_or_404
from .models import Product
from django.urls import reverse
from django.http import JsonResponse
from .models import Category, Product, Cart, CartItem, Order, OrderItem
from django.contrib.auth.decorators import login_required




@login_required(login_url="/admin")
def index(request):
    products = Product.objects.all()
    
    #get count of cartitems
    try:
        cart = Cart.objects.get(user=request.user)
        cartitems = CartItem.objects.filter(cart=cart).values('product').distinct().count()
    except Cart.DoesNotExist:
        cart = None
        cartitems = 0
    print(cartitems)
    #End of get count of cartitems
    return render(request, 'index.html', {'products': products,'cartitems':cartitems})


@login_required
def add_to_cart(request, product_id):
    productID = request.POST['input_field']
    
    #create a cart instance
    try:
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        Cart.objects.create(user=request.user)

    
    #add cart item
    cartItemInstance = CartItem(cart=Cart.objects.get(user=request.user),product=Product.objects.get(id=productID))
    cartItemInstance.save()
    
    response_data = {
            'message': 'Data received',
            'input_field': productID,
            'status': 'success'
        }
    return JsonResponse(response_data)


@login_required
def cart(request):
    try:
        cart = Cart.objects.get(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)
        for item in cart_items:
            item.total_price = item.product.price * item.quantity
        total_cart_value = sum(item.total_price for item in cart_items)
    except Cart.DoesNotExist:
        cart = None
        cart_items = []
        total_cart_value = 0

    context = {
        'cart': cart,
        'cart_items': cart_items,
        'total_cart_value': total_cart_value
    }
    return render(request, 'cart.html', context)

@login_required
def checkout(request):
    # Handle the checkout process
    return render(request, 'checkout.html')

@login_required
def delete_item(request, id):
    if request.method == 'DELETE':
        cart_item = get_object_or_404(CartItem, id=id)
        cart_item.delete()
        return JsonResponse({"response": "success"})
    return JsonResponse({"response": "error"}, status=400)

@login_required
def confirmed_order(request):
    if request.method =="POST":
        token = request.POST["csrfmiddlewaretoken"]
        if token:
            #check if curret user has a cart
            try:
                cart = Cart.objects.get(user=request.user)
            except:
                cart = None
            
            #if user has a cart, check if the cart has items
            if cart:
                cart_items = CartItem.objects.filter(cart=cart)
                if cart_items:
                    #get total amount
                    total_cart_value = sum(item.product.price * item.quantity for item in cart_items)
                    #create  order
                    order_instance = Order(user=request.user,total_price=total_cart_value)
                    order_instance.save()
                    
                    #mMove cart items to order items
                    for cart_item in cart_items:
                        order_item_instance = OrderItem.objects.create(order=order_instance,product=cart_item.product,quantity=cart_item.quantity)
                    
                    #empty cart on order save
                    cart_items.delete()
            else:
                cart_items = []
            
            return redirect("/")
        
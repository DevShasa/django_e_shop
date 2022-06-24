from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Product
from .cart import Cart 
from .forms import CartAddProductForm

@require_POST # Only allow POST requests 
def cart_add(request,product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    # Take contents of request.post and pass them to CartAddProductForm 
    form = CartAddProductForm(request.POST) # Fetch post object from request body 
    if form.is_valid():
        cartData = form.cleaned_data
        # this will append cart item to session session.cart.{products}
        cart.add(
            product=product, 
            quantity=cartData['quantity'], 
            override_quantity=cartData['override']
        )
    
    return redirect('cart:cart_detail')

@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)

    return redirect('cart:cart_detail')

def cart_detail(request):
    '''
    Get the current cart and display it
    '''
    cart = Cart(request)
    for item in cart:
        # add a new entry for every product in cart
        item['update_quantity_form'] = CartAddProductForm(initial={
            'quantity': item['quantity'],
            'override': True
        })
    return render(request, 'cart/detail.html', {'cart': cart})

# The form in the cart detailview will have override true
# The form in the product detailview has ovveride off 
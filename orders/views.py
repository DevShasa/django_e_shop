from django.shortcuts import render
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart

# The view that displays the form to the user 
def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save() # Create a new order object 
            for item in cart:
                OrderItem.objects.create(
                    order = order,
                    product = item['product'],
                    price = item['price'],
                    quantity = item['quantity'],
                )
            # Clear the cart 
            cart.clear()
            # Sucessful redirect here 
            return render(request, 'orders/order/created.html', {'order': order})
    else:
        form = OrderCreateForm()
    
    return render(request, 'orders/order/create.html', {'cart':cart, 'form': form})
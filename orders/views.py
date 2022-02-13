from django.shortcuts import render, redirect
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from .tasks import order_created
from django.urls import reverse


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

            # Launch asynchronous task
            order_created.delay(order.id)
            # Set the order in the session
            request.session['order_id'] = order.id
            # Redirect for payment
            return redirect(reverse('payment:process'))

            # # Sucessful redirect here 
            # return render(request, 'orders/order/created.html', {'order': order})
    else:
        form = OrderCreateForm()
    
    return render(request, 'orders/order/create.html', {'cart':cart, 'form': form})
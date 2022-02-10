from .cart import Cart

def cart(request):
    '''
    Instantiate cart using request object 
    Make it available to templates as a variable named cart
    '''
    return {
        'cart': Cart(request) # Fetch the session or create one if it does not exist
    }
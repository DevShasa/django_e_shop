from decimal import Decimal
from django.conf import settings
from shop.models import Product 

class Cart(object):

    def __init__(self, request):
        """
        settings.CART_SESSION_ID = 'cartr'
        Initialise the cart
        request = { session, headers,body,}
        session = {cart, modified}

        cart dictionay will look like this
        cart = {
            'product_id': {'price': price, 'quantity': quantity},
        }
        """
        self.session = request.session
        # get the session object
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # Save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
            self.cart  = cart

        def add(self, product, quantity=1, override_quantity=False):
            '''
            Add a product to the cart to update its quantity 
            '''
            product_id = str(product.id) #cos id is an integer
            if product_id not in self.cart:
                self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}

            if override_quantity:
                self.cart[product_id]['quantity'] = quantity
            else:
                self.cart[product_id]['quantity'] += quantity
            
            self.save()
        
        def save(self):
            # Mark the session as modified to make sure it gets saved
            # each session comes with a modified attribute, changing it ti true...
            # ..prompts django to save the session
            self.session.modified = True
        
        def remove(self, product):
            '''
            Remove a product from the cart
            '''
            product_id = str(product.id)
            if product_id in self.cart:
                del self.cart[product_id]
                self.save()
        
        def __iter__(self):
            '''
            Iterate over the items in the cart, to get the products from the database
            '''
            product_ids = self.cart.keys()
            products = Product.objects.filter(id__in=product_ids)

            cart = self.cart.copy()
            for product in products:
                # Add a product field to cart
                cart[str(product.id)]['product'] = product
            
            for item in cart.values():
                '''
                Cart now looks like this
                cart={
                    product_id:{price, quantity, product }
                }
                '''
                item['price'] = Decimal(item['price'])
                item['total_price'] = item['price'] * item['quantity']
                
                yield item
            
        def __len__(self):
            '''
            Count all the items in the cart
            '''
            return sum(item['quantity'] for item in self.cart.values())

        def get_total_price(self):
            '''
            Count the price of all items in the cart
            '''
            return sum(Decimal(item['price'] * item['quantity']) for item in cart.values())
        
        def clear(self):
            # Remove the cart from session
            del self.session[settings.CART_SESSION_ID]
            self.save()
from celery import task 
from django.core.mail import send_mail
from .models import Order

@task
def order_created(order_id):
    '''
    Task to send an email notification when an order is 
    Sucessfully created 
    '''
    order = Order.objects.get(id=order_id)
    subject = f'ORDER NUMBER: {order.id}'
    message = f'Dear {order.first_name}, \n\n' \
                f'You have successfully placed an order.' \
                    f'Your order ID is {order.id}'
    mail_sent = send_mail(subject, message, 'admin@myshop.com', [order.email])

    return mail_sent
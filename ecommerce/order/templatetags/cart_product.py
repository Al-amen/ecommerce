from django import template
from order.models import Cart,Order
from django.contrib.auth.models import AnonymousUser

register = template.Library()

@register.filter
def cart_view(user):
    cart=Cart.objects.filter(user=user,purchased=False)
    if cart.exists():
     return cart
    
    else: cart
    
# @register.filter
# def cart_total(user):
#     order = Order.objects.filter(user=user, ordered=False)
#     if order.exists():
#        return order[0].get_totals()
#     else: 
#        return 0



@register.filter
def cart_total(user):
    # Check if the user is authenticated
    if not hasattr(user, 'is_authenticated') or not user.is_authenticated:
        return 0  # Return 0 for anonymous users

    # If authenticated, get the user's active (non-ordered) order
    order = Order.objects.filter(user=user, ordered=False)
    if order.exists():
        return order[0].get_totals()
    
    return 0  # Return 0 if no order exists

# @register.filter
# def cart_count(user):
#     order = Order.objects.filter(user=user,ordered=False)
#     if order.exists():
#        return order[0].order_items.count()

#     else:
#        return 0


@register.filter
def cart_count(user):
    # Ensure we are working with the actual User or AnonymousUser object
    if not hasattr(user, 'is_authenticated') or not user.is_authenticated:
        return 0
    
    # Otherwise, query the Order model
    order = Order.objects.filter(user=user, ordered=False)
    if order.exists():
        return order[0].order_items.count()
    
    return 0
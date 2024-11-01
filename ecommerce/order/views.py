from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages  # Import messages framework
from store.models import Product
from order.models import Cart, Order, WishList
from coupon.models import Coupon
from coupon.forms import CouponCodeForm
from django.utils import timezone
from notification.notific import SendNotification

# Create your views here.

def add_to_cart(request, pk):
    if request.user.is_authenticated:
        item = get_object_or_404(Product, pk=pk)
        try:
            order_item, created = Cart.objects.get_or_create(item=item, user=request.user, purchased=False)
            order_qs = Order.objects.filter(user=request.user, ordered=False)

            if order_qs.exists():
                order = order_qs[0]
                if order.order_items.filter(item=item).exists():
                    color = request.POST.get('color')
                    size = request.POST.get('size')
                    quantity = request.POST.get('quantity')

                    order_item.quantity += int(quantity) if quantity else 1
                    order_item.color = color
                    order_item.size = size
                    order_item.save()
                    messages.success(request, "Quantity updated successfully!")
                    SendNotification(request.user, "Quantity updated")
                else:
                    order_item.color = request.POST.get('color')
                    order_item.size = request.POST.get('size')
                    order_item.save()
                    order.order_items.add(order_item)
                    messages.success(request, "Product added to your cart!")

                next_url = request.GET.get('next', 'store:index')
                return redirect(next_url)
            else:
                new_order = Order.objects.create(user=request.user)
                new_order.order_items.add(order_item)
                messages.success(request, "Product added to your cart!")
                SendNotification(request.user, "Product added to your cart")
                next_url = request.GET.get('next', 'store:index')
                return redirect(next_url)
        except Exception as e:
            messages.error(request, "An error occurred while adding the item to your cart. Please try again.")
            next_url = request.GET.get('next', 'store:index')
            return redirect(next_url)
    else:
        messages.warning(request, "You need to log in to add items to your cart.")
        return redirect('account:login')



def cart_view(request):
    if not request.user.is_authenticated:
        messages.warning(request, "You need to log in to view your cart.")
        return redirect('account:login')

    # Get user's cart and pending order
    carts = Cart.objects.filter(user=request.user, purchased=False)
    orders = Order.objects.filter(user=request.user, ordered=False)

    if not carts.exists() or not orders.exists():
        messages.warning(request, "Your cart is empty.")
        return redirect('store:index')

    # Initialize coupon, total discount, and subtotal
    order = orders[0]
    coupon_form = CouponCodeForm(request.POST or None)
    coupon_code = None
    total_price_after_discount = None
    subtotal = 0
    print(carts)
    for cart in carts:
       total = cart.get_total()
       #print(f"Total for {cart.item.name}: {total} (type: {type(total)})")  # Debugging output
       subtotal += float(total)
    # Apply coupon if form is submitted and valid
    if coupon_form.is_valid():
        code = coupon_form.cleaned_data.get('code')
        current_time = timezone.now()

        try:
            coupon_obj = Coupon.objects.get(code=code, active=True)
            
            # Check if the coupon is valid in the current time window
            if coupon_obj.valid_from <= current_time <= coupon_obj.valid_to:
                discount = (coupon_obj.discount / 100) * subtotal  # Calculate discount
                total_price_after_discount = subtotal - discount  # Calculate total after discount
                coupon_code = code

                # Store the discount total and coupon code in the session
                request.session['discount_total'] = total_price_after_discount
                request.session['coupon_code'] = code

                messages.success(request, f"Coupon '{code}' applied successfully!")
            else:
                # Deactivate expired coupon
                coupon_obj.active = False
                coupon_obj.save()
                messages.warning(request, "This coupon is no longer valid.")
        except Coupon.DoesNotExist:
            messages.error(request, "Invalid coupon code.")

    # Retrieve session data if available
    if 'discount_total' in request.session:
        total_price_after_discount = request.session['discount_total']
        coupon_code = request.session.get('coupon_code')
    print(f"after-subtotal{subtotal}")
    # Render cart template with context
    context = {
        'carts': carts,
        'order': order,
        'coupon_form': coupon_form,
        'coupon_code': coupon_code,
        'subtotal': subtotal,
        'total_price_after_discount': total_price_after_discount,
    }
    return render(request, 'store/cart.html', context)






def remove_item_from_cart(request, pk):
    item = get_object_or_404(Product, pk=pk)
    orders = Order.objects.filter(user=request.user, ordered=False)
    try:
        if orders.exists():
            order = orders[0]
            if order.order_items.filter(item=item).exists():
                order_item = Cart.objects.filter(item=item, user=request.user, purchased=False).first()
                order.order_items.remove(order_item)
                order_item.delete()
                messages.success(request, "Item removed from your cart.")
                return redirect('order:cart')
            else:
                messages.warning(request, "Item not found in your cart.")
                return redirect('order:cart')
        else:
            messages.warning(request, "No active order found.")
            return redirect('order:cart')
    except Exception as e:
        messages.error(request, "An error occurred while removing the item from your cart. Please try again.")
        return redirect('order:cart')


def increase_cart(request, pk):
    item = get_object_or_404(Product, pk=pk)
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    try:
        if order_qs.exists():
            order = order_qs[0]
            if order.order_items.filter(item=item).exists():
                order_item = Cart.objects.filter(item=item, user=request.user, purchased=False).first()
                if order_item:
                    order_item.quantity += 1
                    order_item.save()
                    print(f"orderitemQ {order_item.quantity}")
                    
                    print(f"Order Total after update (increase): {order.get_totals()}")
                    messages.success(request, "Item quantity increased.")
                return redirect('order:cart')
            else:
                messages.warning(request, "Item not found in your cart.")
                return redirect('store:index')
        else:
            messages.warning(request, "No active order found.")
            return redirect('store:index')
    except Exception as e:
        messages.error(request, "An error occurred while increasing the item quantity. Please try again.")
        return redirect('store:index')


def decrease_cart(request, pk):
    item = get_object_or_404(Product, pk=pk)
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    try:
        if order_qs.exists():
            order = order_qs[0]
            if order.order_items.filter(item=item).exists():
                order_item = Cart.objects.filter(item=item, user=request.user, purchased=False).first()
                if order_item:
                    if order_item.quantity > 1:
                        order_item.quantity -= 1
                        order_item.save()
                        
                        messages.success(request, "Item quantity decreased.")
                    else:
                        order.order_items.remove(order_item)
                        order_item.delete()
                    
                    messages.success(request, "Item removed from your cart.")
                return redirect('order:cart')
            else:
                messages.warning(request, "Item not found in your cart.")
                return redirect('store:index')
        else:
            messages.warning(request, "No active order found.")
            return redirect('store:index')
    except Exception as e:
        messages.error(request, "An error occurred while decreasing the item quantity. Please try again.")
        return redirect('store:index')




def add_to_wishlist(request,pk):
    product = get_object_or_404(Product, pk=pk)
    wishlist_item, created = WishList.objects.get_or_create(user=request.user, product=product)
    
    if created:
        messages.success(request, "Product added to wishlist.")
    else:
        messages.info(request, "Product is already in your wishlist.")
    
    next_url = request.GET.get('next', 'store:index')
    return redirect(next_url)


def view_wishlist(request):
    wishlist_items = WishList.objects.filter(user=request.user)
    print(wishlist_items)
    return render(request, 'store/wishlist.html', {'wishlist_items': wishlist_items})


def remove_from_wishlist(request, pk):
    if request.user.is_authenticated:
        print(f"Trying to remove product with pk={pk} from wishlist for user {request.user}")
        wishlist_item = get_object_or_404(WishList, product__pk=pk, user=request.user)
        wishlist_item.delete()
        return redirect('order:view_wishlist')
    else:
        return redirect('account:login')


import os
from io import BytesIO
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.utils import timezone
from django.conf import settings
from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404, redirect
from order.models import Order
from django.urls import reverse
import logging

logger = logging.getLogger(__name__)

def generate_invoice(request, order_id):
    if not request.user.is_authenticated:
        return redirect('login')

    try:
       
        order = get_object_or_404(Order, user=request.user, order_id=order_id)

        buffer = BytesIO()
       
        p = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter

        p.drawString(100, height - 50, "Invoice")
        p.drawString(100, height - 70, f"Order ID: {order.order_id}")
        p.drawString(100, height - 90, f"Date: {timezone.now().date()}")

        y_position = height - 130
        p.drawString(100, y_position, "Ordered Products:")
        y_position -= 20

        for item in order.get_ordered_items():
            p.drawString(100, y_position, f"{item['quantity']} X {item['product_name']}")
            p.drawString(300, y_position, f"${item['total_price']}")
            y_position -= 20


        p.drawString(100, y_position - 20, f"Total: ${order.get_totals()}")

        p.showPage()
        p.save()

        pdf_data = buffer.getvalue()
        buffer.close()


        invoice_dir = os.path.join(settings.MEDIA_ROOT, 'invoices')
        if not os.path.exists(invoice_dir):
            os.makedirs(invoice_dir)
        invoice_filename = f"invoice_{order_id}.pdf"
        invoice_path = os.path.join(invoice_dir, invoice_filename)
        with open(invoice_path, 'wb') as f:
            f.write(pdf_data)

        # Send the invoice via email
        email_subject = 'Your Invoice from Our Store'
        email_message = 'Please find attached your invoice.'
        email = EmailMessage(
            subject=email_subject,
            body=email_message,
            to=[request.user.email]
        )
        email.attach(invoice_filename, pdf_data, 'application/pdf')
        email.send()

        logger.info(f"Invoice for Order {order_id} has been generated and sent to {request.user.email}.")

        return redirect(reverse('store:index'))

    except Exception as e:
        logger.error(f"Error generating invoice for order {order_id}: {e}")
        return HttpResponse("An error occurred while generating the invoice.", status=500)

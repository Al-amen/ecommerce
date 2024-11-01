from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.conf import settings
from django.urls import reverse
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from decimal import Decimal

from payment.models import BillingAddress
from payment.forms import BillingAddressForm, PaymentMethodForm
from order.models import Cart, Order
from pysslcmz.payment import SSLCSession
from store.models import VariationValue

class CheckBillingAddressView(TemplateView):
    template_name = "store/checkout.html"
    
    def get(self, request, *args, **kwargs):
        saved_address, _ = BillingAddress.objects.get_or_create(user=request.user)
        form = BillingAddressForm(instance=saved_address)
        order_qs = Order.objects.filter(user=request.user, ordered=False).first()
        carts = Cart.objects.filter(user=request.user, purchased=False)
        subtotal = 0

        if not order_qs:
            return redirect('order:cart')
        else:
            for cart in carts:
               total = cart.get_total()
               print(f"Total for {cart.item.name}: {total} (type: {type(total)})")  # Debugging output
               subtotal += float(total)
        context = {
            'billing_address': form,
            'order_item': order_qs.order_items.all(),
            'order_total':   subtotal ,        #order_qs.get_totals(),   
            'payment_method': PaymentMethodForm(),
            'pay_meth': request.GET.get('pay_meth'),
            'carts':carts
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        saved_address, _ = BillingAddress.objects.get_or_create(user=request.user)
        form = BillingAddressForm(request.POST, instance=saved_address)
        payment_obj = Order.objects.filter(user=request.user, ordered=False).first()
        carts = Cart.objects.filter(user=request.user, purchased=False)
        subtotal = 0
        if not payment_obj:
            return redirect('order:cart')
        else :
             for cart in carts:
               total = cart.get_total()
               print(f"Total for {cart.item.name}: {total} (type: {type(total)})")  # Debugging output
               subtotal += float(total)

        pay_form = PaymentMethodForm(request.POST, instance=payment_obj)
        if form.is_valid() and pay_form.is_valid():
            form.save()
            pay_method = pay_form.save()
            if not saved_address.is_fully_filled():
                messages.error(request, "Please fill in all billing address fields.")
                return redirect('payment:checkout')

            order = payment_obj

            if pay_method.payment_method == 'Cash on Delivery':
                self._complete_order(request, order, pay_method.payment_method)
                messages.success(request, "Order submitted successfully!")
                return redirect('store:index')

            if pay_method.payment_method == "SSLcommerz":
                return self._process_ssl_commerz(request, order)

        context = {
            'billing_address': form,
            'order_item': payment_obj.order_items.all(),
            'order_total': subtotal,                                     #payment_obj.get_totals(),
            'payment_method': pay_form,
        }
        return render(request, self.template_name, context)

    def _process_ssl_commerz(self, request, order):
        store_id = settings.SSL_STORE_ID
        store_pass = settings.SSL_PASS
        mypayment = SSLCSession(sslc_is_sandbox=True, sslc_store_id=store_id, sslc_store_pass=store_pass)

        status_url = request.build_absolute_uri(reverse('payment:status'))
        mypayment.set_urls(success_url=status_url, fail_url=status_url, cancel_url=status_url, ipn_url=status_url)

        mypayment.set_product_integration(
            total_amount=Decimal(order.get_totals()),
            currency='BDT',
            product_category='clothing',
            product_name=[str(item.item.name) for item in order.order_items.all()], 
            num_of_item=order.order_items.count(),
            shipping_method='Courier',
            product_profile='None'
        )

        current_user = request.user
        mypayment.set_customer_info(
            name=current_user.profile.full_name,
            email=current_user.profile.email or "defaultemail@example.com",
            address1=current_user.profile.address,
            address2=current_user.profile.address,
            city=current_user.profile.city,
            postcode=current_user.profile.zipcode,
            country=current_user.profile.country,
            phone=current_user.profile.phone
        )

        billing_address = BillingAddress.objects.filter(user=request.user).first()
        mypayment.set_shipping_info(
            shipping_to=billing_address.address1,
            address=billing_address.address2,
            city=billing_address.city,
            postcode=billing_address.zipcode,
            country=billing_address.country_name
        )

        response_data = mypayment.init_payment()
        return redirect(response_data['GatewayPageURL'])

    def _complete_order(self, request, order, payment_id):
        order.ordered = True
        order.order_id = order.id
        order.payment_id = payment_id
        order.save()

        cart_items = Cart.objects.filter(user=request.user, purchased=False)
        for item in cart_items:
            try:
                if item.size or item.color:
                    self._manage_stock_for_variation(item)
                    print(item.size,item.color)
                else:
                    item.item.decrease_stock(item.quantity)
                item.purchased = True
                item.save()
            except ValueError as e:
                messages.error(request, f"Stock error: {e}")
                return redirect('order:cart')

    def _manage_stock_for_variation(self, item):
        # Manage stock based on specific variations
        size_variation = VariationValue.objects.filter(product=item.item, variation='size', name=item.size).first()
        color_variation = VariationValue.objects.filter(product=item.item, variation='color', name=item.color).first()
        print(f"Found size variation: {size_variation}, color variation: {color_variation}")
        if size_variation:
            size_variation.decrease_stock(item.quantity)
        if color_variation:
            color_variation.decrease_stock(item.quantity)


@csrf_exempt
def sslc_status(request):
    if request.method == 'POST':
        payment_data = request.POST
        val_id = payment_data['val_id']
        tran_id = payment_data['tran_id']
        return HttpResponseRedirect(reverse('payment:sslc_complete', kwargs={'val_id': val_id, 'tran_id': tran_id}))

    return render(request, 'status.html')


def sslc_complete(request, val_id, tran_id):
    order = Order.objects.filter(user=request.user, ordered=False).first()
    if order:
        order.ordered = True
        order.order_id = val_id
        order.payment_id = tran_id
        order.save()

        cart_items = Cart.objects.filter(user=request.user, purchased=False)
        for item in cart_items:
            try:
                if item.size or item.color:
                    CheckBillingAddressView._manage_stock_for_variation(item)
                else:
                    item.item.decrease_stock(item.quantity)
                item.purchased = True
                item.save()
            except ValueError as e:
                messages.error(request, f"Stock error: {e}")
                print(e)
                return redirect('order:cart')

        return redirect('invoice:generate_invoice', order_id=order.order_id)

    messages.error(request, "Order not found.")
    return redirect('store:index')

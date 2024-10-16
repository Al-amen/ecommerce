# from django.shortcuts import render,redirect
# from django.http import HttpResponseRedirect

# #models
# from payment.models import BillingAddress
# from payment.forms import BillingAddressForm,PaymentMethodForm
# from order.models import Cart,Order

# #view
# from django.views.generic import TemplateView

# # Create your views here.

# class CheckBillingAddressView(TemplateView):
#     template_name = "store/checkout.html"

#     def get(self, request, *args, **kwargs):
#         saved_address = BillingAddress.objects.get_or_create(user=request.user or None)
#         saved_address = saved_address[0]
#         form = BillingAddressForm(instance=saved_address)
#         payment_method = PaymentMethodForm()
#         order_qs = Order.objects.filter(user=request.user, ordered=False)
#         order_item = order_qs[0].order_items.all()
#         order_total = order_qs[0].get_totals()

#         context = {
#             'billing_address':form,
#             'order_item' : order_item,
#             'order_total' : order_total,
#             'payment_method':  payment_method,
#         }
#         return render(request, self.template_name, context=context)
    


#     def post(self, request, *args, **kwargs):

#         saved_address = BillingAddress.objects.get_or_create(user=request.user or None)
#         saved_address = saved_address[0]
#         form = BillingAddressForm(instance=saved_address)
#         payment_obj = Order.objects.filter(user=request.user,ordered=False)[0]
#         payment_form = PaymentMethodForm(instance=payment_obj)
        
#         if request.method == 'post' or request.method == 'POST':
#             form = BillingAddressForm(request.POST,instance=saved_address)
#             pay_form = PaymentMethodForm(request.POST, instance=payment_obj)
#             if form.is_valid() and payment_form.is_valid():
#                 form.save()
#                 pay_method = pay_form.save()
#                 pay_method.save()
#                 return redirect('order:cart')



from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from payment.models import BillingAddress
from payment.forms import BillingAddressForm, PaymentMethodForm
from order.models import Cart, Order
from django.views.generic import TemplateView


class CheckBillingAddressView(TemplateView):
    template_name = "store/checkout.html"

    def get(self, request, *args, **kwargs):
        # Fetch or create the user's billing address
        saved_address = BillingAddress.objects.get_or_create(user=request.user or None)[0]
        form = BillingAddressForm(instance=saved_address)

        # Fetch the current unpaid order and its items
        order_qs = Order.objects.filter(user=request.user, ordered=False).first()
        
        # Handle the case where no unpaid order exists
        if not order_qs:
            return redirect('order:cart')  # or another page if needed

        order_items = order_qs.order_items.all()
        order_total = order_qs.get_totals()

        # Payment method form
        payment_method = PaymentMethodForm()

        # Prepare context for rendering
        context = {
            'billing_address': form,
            'order_item': order_items,
            'order_total': order_total,
            'payment_method': payment_method,
        }

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        # Fetch or create the user's billing address
        saved_address = BillingAddress.objects.get_or_create(user=request.user or None)[0]
        form = BillingAddressForm(request.POST, instance=saved_address)

        # Fetch the current unpaid order
        payment_obj = Order.objects.filter(user=request.user, ordered=False).first()
        
        if not payment_obj:
           return redirect('order:cart')
 # Redirect if no unpaid order

        pay_form = PaymentMethodForm(request.POST, instance=payment_obj)

        # Validate the forms
        if form.is_valid() and pay_form.is_valid():
            form.save()
            pay_method = pay_form.save()
            if not saved_address.is_fully_filled():
                print("working")
                return redirect('payment:checkout')  


            #cash on delivery payment process
            if pay_method.payment_method == 'Cash on Delivery':
                order_qs = Order.objects.filter(user=request.user, ordered=False)
                order = order_qs[0]
                order.ordered=True
                order.order_id = order.id      
                order.payment_id = pay_method.payment_method
                order.save()
                cart_items = Cart.objects.filter(user=request.user, purchased=False)
                for item in cart_items:
                    item.purchased = True
                    item.save()
                print('order summited successfully')
                return redirect('store:index')


        # If forms are not valid, render the page with errors
        context = {
            'billing_address': form,
            'order_item': payment_obj.order_items.all(),
            'order_total': payment_obj.get_totals(),
            'payment_method': pay_form,
        }
        return render(request, self.template_name, context)

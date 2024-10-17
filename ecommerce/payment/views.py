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
from django.conf import settings
from django.urls import reverse
from payment.models import BillingAddress
from payment.forms import BillingAddressForm, PaymentMethodForm
from order.models import Cart, Order
from django.views.generic import TemplateView


class CheckBillingAddressView(TemplateView):
    template_name = "store/checkout.html"

    def get(self, request, *args, **kwargs):
        saved_address = BillingAddress.objects.get_or_create(user=request.user or None)[0]
        form = BillingAddressForm(instance=saved_address)
        order_qs = Order.objects.filter(user=request.user, ordered=False).first()
        
        if not order_qs:
            return redirect('order:cart')  # or another page if needed

        order_items = order_qs.order_items.all()
        order_total = order_qs.get_totals()
        payment_method = PaymentMethodForm()
         
        pay_meth = request.GET.get('pay_meth')

        context = {
            'billing_address': form,
            'order_item': order_items,
            'order_total': order_total,
            'payment_method': payment_method,
            'paypal_client_id': settings.PAYPAL_CLIENT_ID,
            'pay_meth': pay_meth ,
        }

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
       
        saved_address = BillingAddress.objects.get_or_create(user=request.user or None)[0]
        form = BillingAddressForm(request.POST, instance=saved_address)
        payment_obj = Order.objects.filter(user=request.user, ordered=False).first()
        
        if not payment_obj:
           return redirect('order:cart')
        pay_form = PaymentMethodForm(request.POST, instance=payment_obj)


        if form.is_valid() and pay_form.is_valid():
            form.save()
            pay_method = pay_form.save()
            if not saved_address.is_fully_filled():
                print("working")
                return redirect('payment:checkout')  


        
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
            
            if pay_method.payment_method == "PayPal":
                return redirect(reverse('payment:checkout') + "?pay_meth=" + str(pay_method.payment_method))
            
                
        # If forms are not valid, render the page with errors
        context = {
            'billing_address': form,
            'order_item': payment_obj.order_items.all(),
            'order_total': payment_obj.get_totals(),
            'payment_method': pay_form,
        }
        return render(request, self.template_name, context)
    






# def paypalPaymentMethod(request):
#     data = json.loads(request.body)
#     order_id = data['order_id']
#     payment_id = data['payment_id']
#     status = data['status']
#     if status == "COMPLETED":
#         if request.user.is_authenticated:
#                 order_qs = Order.objects.filter(user=request.user, ordered=False)
#                 order = order_qs[0]
#                 order.ordered=True
#                 order.order_id = order_id      
#                 order.payment_id = payment_id
#                 order.save()
#                 cart_items = Cart.objects.filter(user=request.user, purchased=False)
#                 for item in cart_items:
#                     item.purchased = True
#                     item.save()
                
#                 return redirect('store:index')



import json
from django.http import JsonResponse
from django.shortcuts import redirect


def paypalPaymentMethod(request):
    if request.method == "POST":
        try:
            # Parse the JSON data from the request body
            data = json.loads(request.body)
            order_id = data.get('order_id')
            payment_id = data.get('payment_id')
            status = data.get('status')

            # Ensure all necessary fields are provided
            if not order_id or not payment_id or not status:
                return JsonResponse({'error': 'Missing required payment data.'}, status=400)

            # Proceed only if payment status is "COMPLETED"
            if status == "COMPLETED":
                if request.user.is_authenticated:
                    # Retrieve the user's active order that hasn't been marked as ordered
                    order_qs = Order.objects.filter(user=request.user, ordered=False)

                    # Ensure there's an active order
                    if order_qs.exists():
                        order = order_qs.first()  # Safely get the first order

                        # Update the order with payment details and mark it as ordered
                        order.ordered = True
                        order.order_id = order_id
                        order.payment_id = payment_id
                        order.save()

                        # Mark the user's cart items as purchased
                        cart_items = Cart.objects.filter(user=request.user, purchased=False)
                        for item in cart_items:
                            item.purchased = True
                            item.save()

                        # Redirect to store index after successful payment
                        return redirect('store:index')

                    else:
                        return JsonResponse({'error': 'No open order found for this user.'}, status=400)
                else:
                    return JsonResponse({'error': 'User not authenticated.'}, status=401)

            # Return error if payment was not completed successfully
            return JsonResponse({'error': 'Payment not completed.'}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data.'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method.'}, status=400)

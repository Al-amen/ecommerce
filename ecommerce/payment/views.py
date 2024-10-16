from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect

#models
from payment.models import BillingAddress
from payment.forms import BillingAddressForm
from order.models import Cart,Order

#view
from django.views.generic import TemplateView

# Create your views here.

class CheckBillingAddressView(TemplateView):
    template_name = "store/checkout.html"

    def get(self, request, *args, **kwargs):
        saved_address = BillingAddress.objects.get_or_create(user=request.user or None)
        saved_address = saved_address[0]
        form = BillingAddressForm(instance=saved_address)
        
        order_qs = Order.objects.filter(user=request.user, ordered=False)
        order_item = order_qs[0].order_items.all()
        order_total = order_qs[0].get_totals()

        context = {
            'billing_address':form,
            'order_item' : order_item,
            'order_total' : order_total,
        }
        return render(request, self.template_name, context=context)
    
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Field
from .models import BillingAddress
from order.models import Order
class BillingAddressForm(forms.ModelForm):
    class Meta:
        model = BillingAddress
        #fields = ['first_name', 'last_name', 'country_name','city', 'address1','address2', 'zipcode', 'phone_number']
        fields = '__all__'
        exclude = ('user',)
    

class PaymentMethodForm(forms.ModelForm):
     class Meta:
         model = Order
         fields = ['payment_method']
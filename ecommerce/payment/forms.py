from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Field
from .models import BillingAddress
class BillingAddressForm(forms.ModelForm):
    class Meta:
        model = BillingAddress
        fields = ['first_name', 'last_name', 'country_name', 'address1','address2', 'zipcode', 'phone_number']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Crispy form helper
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('first_name', css_class='col-sm-6'),
                Column('last_name', css_class='col-sm-6'),
                css_class='row'
            ),
            Field('country_name', css_class='form-control'),
            Field('address1', placeholder='House number and Street name', css_class='form-control'),
            Field('address2', placeholder='Appartments, suite, unit etc ...', css_class='form-control'),
            Row(
                Column('zipcode', css_class='col-sm-6'),
                Column('phone_number', css_class='col-sm-6'),
                css_class='row'
            )
        )

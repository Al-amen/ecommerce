from django import forms



class CouponCodeForm(forms.Form):
    code = forms.CharField(
          widget=forms.TextInput(attrs={
            'placeholder': 'Coupon code',  # Set the placeholder text
            'style': 'text-align: center;'  # Inline style to center text
        })
    )
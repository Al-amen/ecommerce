from django.urls import path
from payment import views

app_name = 'payment'

urlpatterns = [
    #  path('ok/', views.billingaddress, name='baku'),
    path('checkout/', views.CheckBillingAddressView.as_view(),name='checkout'),
]


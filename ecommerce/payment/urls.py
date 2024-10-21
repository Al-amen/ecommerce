from django.urls import path
from payment import views

app_name = 'payment'

urlpatterns = [
    #  path('ok/', views.billingaddress, name='baku'),
    path('checkout/', views.CheckBillingAddressView.as_view(),name='checkout'),
    #path('paypal/',views.paypalPaymentMethod,name='paypal_payment'),
    path("sslc/status/",views.sslc_status,name="status"),
    path("sslc/complete<val_id>/<tran_id>/",views.sslc_complete,name="sslc_complete"),
   
]


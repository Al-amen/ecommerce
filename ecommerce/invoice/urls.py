from django.urls import path
from invoice import views

app_name = 'invoice'

urlpatterns = [
     path('invoice/<str:order_id>/', views.generate_invoice, name='generate_invoice'),
]

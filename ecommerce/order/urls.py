from django.urls import path
from order import views

app_name = "order"
urlpatterns = [

    path('add_to_cart/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('cart_veiw/',views.cart_view, name='cart'),
    path('remove-item/<int:pk>/',views.remove_item_from_cart, name='remove-item'),
    path('increase<int:pk>/',views.increase_cart, name='increase'),
    path('decrease/<int:pk>/',views.decrease_cart, name='decrease'),


    
]

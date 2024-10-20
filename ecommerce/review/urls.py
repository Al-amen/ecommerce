from django.urls import path
from review import views

app_name = 'review'

urlpatterns = [
    path('submit_review/<int:product_id>/', views.submit_review, name='submit_review'),
]



from django.urls import path
from account import views

app_name = "account"
urlpatterns = [
    path('register/',views.register, name='register'),
    path('login/',views.Customerlogin,name='login'),
    path('logout/',views.logout_view, name="logout"),
    path('profile/',views.ProfileView.as_view(),name='profile'),
    path('account-verify/<str:token>/', views.account_verify, name='account_verify')
]

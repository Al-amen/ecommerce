from django.urls import path, reverse_lazy
from account import views
from django.contrib.auth import views as auth_views

app_name = "account"
urlpatterns = [
    path('register/',views.register, name='register'),
    path('login/',views.Customerlogin,name='login'),
    path('logout/',views.logout_view, name="logout"),
    path('profile/',views.ProfileView.as_view(),name='profile'),
    path('account-verify/<str:token>/', views.account_verify, name='account_verify'),
    path('delete-order/<int:order_id>/', views.delete_order, name='delete_order'),

     path('password-reset/', views.ResetPasswordView.as_view(), name='password_reset'),
     path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='account/password_reset_done.html'
         ),
         name='password_reset_done'),
     path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='account/password_reset_confirm.html',success_url=reverse_lazy('account:password_reset_complete')),
         name='password_reset_confirm'),
      path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='account/password_reset_complete.html'),
         name='password_reset_complete'),

]

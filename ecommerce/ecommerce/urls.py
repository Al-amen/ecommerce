
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.contrib.staticfiles.urls import static, staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/',include('account.urls')),
    path('',include('store.urls')),
    path('order/',include('order.urls')),
    # path('coupon/',include('coupon.urls')),
    path('payment/',include('payment.urls')),
    path('notification',include('notification.urls')),
    path('dashboard/',include('dashboard.urls')),
    path('review/',include('review.urls')),
    path('invoice/',include('invoice.urls')),
]

urlpatterns += staticfiles_urlpatterns()

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

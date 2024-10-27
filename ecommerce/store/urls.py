from django.urls import path
from store import views
app_name = 'store'



urlpatterns = [
   path('',views.HomemplateView.as_view(), name='index'),
   path("product/<slug:slug>/",views.ProductDetailView.as_view(),name="product_detail"),
    path('search-results/', views.SearchResultsView.as_view(), name='search_results'),
    
]

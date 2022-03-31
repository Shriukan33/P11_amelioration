from django.urls import path
from .views import (ProductLookupView, ProductLookupResultsView, FavoritesView,
                    ProductDetails, favorite_click, ProductLookupByNameView)

app_name = 'product_lookup'

urlpatterns = [
    path('', ProductLookupView.as_view(), name='product_lookup'),
    path('search/<str:product_name>', ProductLookupResultsView.as_view(),
         name='product_lookup_results'),
    path('product-list/<str:product_name>', ProductLookupByNameView.as_view(),
         name='product_lookup_by_name'),
    path('my-favorites/', FavoritesView.as_view(), name='my_favorites'),
    path('details/<int:pk>/', ProductDetails.as_view(),
         name='product_details'),
    path('ajax/toggle-favorite/<int:product_id>', favorite_click,
         name='favorite_click'),
]

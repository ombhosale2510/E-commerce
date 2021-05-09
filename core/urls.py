from django.urls import path
from .views import *

app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('checkout/', ChecoutView.as_view(), name='checkout'),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('product/<slug>/', ItemDetailView.as_view(), name='product'),
    path('cart_add/<slug>/', add_to_cart, name='cart_add'),
    path('cart_remove/<slug>/', remove_from_cart, name='cart_remove'),
    path('cart_item_remove/<slug>/', remove_single_item_from_cart,
         name='cart_item_remove'),
]

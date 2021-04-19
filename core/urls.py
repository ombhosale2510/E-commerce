from django.urls import path
from .views import *

app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('checkout/', checkout, name='checkout'),
    path('product/<slug>/', ItemDetailView.as_view(), name='product'),
    path('cart/<slug>/', add_to_cart, name='cart'),
    path('cart_remove/<slug>/', remove_from_cart, name='cart_remove'),
]

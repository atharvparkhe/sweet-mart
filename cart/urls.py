from django.urls import path
from . import views
from .views import *

urlpatterns = [
	path('cart/', views.cartPage, name="cart"),
	path('checkout/', views.checkoutPage, name="checkout"),
	path('cart/apply-coupon/<cart_id>/', views.couponApplied, name="apply-coupon"),
	path('success/', views.successPage, name="success"),
	path('failed/', views.failedPage, name="failed"),
	path('select-address/', views.selectAddress, name="select-address"),
]
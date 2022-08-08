from django.urls import path
from . import views
from .views import *

urlpatterns = [
	path('', views.homePage, name="index"),
	path('about/', views.aboutPage, name="about"),
	path('contact/', views.contactPage, name="contact"),
    
	path('blog/<blog_id>/', views.blogPage, name='blog'),
	path('add-blog-comment/<blog_id>/', views.addBlogComment, name='add-blog-comment'),

    path('all-products/', views.allProductsPage, name="all-products"),
	path('product/<product_id>/', views.productPage, name="product"),

	path('add-to-cart/<item_id>/', views.add_to_cart, name="add-to-cart"),
	path('remove-from-cart/<item_id>/', views.remove_from_cart, name="remove-from-cart"),
	path('delete-from-cart/<item_id>/', views.delete_from_cart, name="delete-from-cart"),
]
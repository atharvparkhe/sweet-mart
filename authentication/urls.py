from django.urls import path
from . import views
from .views import *

urlpatterns = [
	path('login/', views.LogIn, name="login"),
	path('signup/', views.SignUp, name="signup"),
	path('verify/<tok>/', views.Verify, name="verify"),
	path('forgot/', views.Forget, name="forgot"),
	path('reset/<token>/', views.Reset, name="reset"),
	path('logout/', views.logoutView, name="logout"),
	path('address/', views.addressView, name="address"),
]
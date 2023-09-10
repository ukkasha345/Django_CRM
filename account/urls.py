from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('loginPage/', views.loginPage, name='loginPage'),
    path('logoutUser/', views.logoutUser, name='logoutUser'),
    path('register/', views.register, name='register'),
    path('products/', views.products, name='products'),
    path('customer/<str:pk_test>', views.customer, name='customer'),
    path('create_order/<str:pk>',views.createOder, name="create_order"),
    path('update_order/<str:pk>',views.updateOrder, name="update_order"),
    path('delete_order/<str:pk>',views.deleteOrder, name="delete_order"),
    
]





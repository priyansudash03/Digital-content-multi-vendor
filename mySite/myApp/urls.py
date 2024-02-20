
from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',index,name="index"),
    path('product/<int:id>',detail,name="detail"),
    path('success/<int:id>',payment_success_view,name="success"),
    path('failed/',payment_failed_view,name="payment_failed_view"),
    path('createproduct/',create_product,name="createproduct"),
    path('editproduct/<int:id>',product_edit,name="editproduct"),
    path('delete/<int:id>',product_delete,name='delete'),
    path('dashboard/',dashboard,name='dashboard'),
    path('register/',register,name='register'),
    path('login/',auth_views.LoginView.as_view(template_name='myApp/login.html'),name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name='myApp/logout.html'),name='logout'),
    path('invalid/',invalid,name='invalid'),
    path('purchases/',my_purchases,name='purchases'),
    path('sales/',sales,name='sales')
    # path('api/checkout/<int:id>',create_checkout,name='api_checkooy')
]

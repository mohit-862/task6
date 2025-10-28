
from django.urls import path
from .views import home,products,user_login,user_logout,user_register,product_details,add_products,seller_dashboard,delete_product,take_query

urlpatterns = [
    #products
    path('',home,name="home"),

    #user paths
    path('products/',products,name="products"),
    path('products/<slug:slug>/',product_details,name="product_details"),
    path('products/take_query',take_query,name="take_query"),


    #seller_paths
    path('add_products/',add_products,name="add_products"),
    path('seller_dashboard',seller_dashboard,name="seller_dashboard"),
    path('delete_product/<int:product_id>',delete_product,name="delete_product"),


    #login,logout,register
    path('user_login/',user_login,name="user_login"),
    path('user_logout/',user_logout,name="user_logout"),
    path('user_register/',user_register,name='user_register'),
]

from django.urls import path
from . import views

urlpatterns = [ 
    path('',views.index,name='index'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('confirm/', views.confirmed_order, name='confirmed_order'),
    path('delete_item/<int:id>/', views.delete_item, name='delete_item'),
   
]
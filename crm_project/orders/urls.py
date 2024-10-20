from django.urls import path
from .views import create_order_view, order_list_view, order_detail_view, edit_order_view

urlpatterns = [
    path('orders/', order_list_view, name='order_list'),
    path('orders/create/', create_order_view, name='create_order'),
    path('orders/<int:pk>/', order_detail_view, name='order_detail'),
    path('orders/<int:pk>/edit/', edit_order_view, name='edit_order'),
]

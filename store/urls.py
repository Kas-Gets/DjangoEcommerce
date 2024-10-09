from django.urls import path
from . import views


urlpatterns = [
    #User Handling
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),

    # Product APIs
    path('products/', views.get_products, name='get_products'),
    path('products/<int:pk>/', views.get_product_detail, name='get_product_detail'),
    path('products/create/', views.create_product, name='create_product'),


    # Customer APIs
    path('customers/', views.get_customers, name='get_customers'),
    path('customers/<int:pk>/', views.get_customer_detail, name='get_customer_detail'),
    path('customers/create/', views.create_customer, name='create_customer'),

      # Orders
    path('orders/', views.get_orders, name='get_orders'),
    path('orders/<int:pk>/', views.get_order_detail, name='get_order_detail'),
    path('orders/create/', views.create_order, name='create_order'),
    path('orders/<int:pk>/update-payment-status/', views.update_order_payment_status, name='update_order_payment_status'),

    # Order Items
    path('order-items/create/', views.create_order_item, name='create_order_item'),

]

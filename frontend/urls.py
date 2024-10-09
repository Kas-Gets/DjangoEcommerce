from django.conf import settings
from django.urls import include, path
# from rest_framework.routers import DefaultRouter
from .views import product_list

from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('get-products/', views.get_products, name='get_products'),
    path('products/', views.product_list, name='product_list'),
    path('products/<int:id>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('loginview/', views.login_view, name='loginview'),
    path('signupview/', views.signup_view, name='signupview'),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]

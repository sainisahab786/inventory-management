from django.urls import path, include
from .views import (
    product_list, product_create, product_update, product_delete,
    add_stock, remove_stock, report,
    user_login, user_logout, register,
    ProductViewSet, StockLogViewSet
)
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'stock_logs', StockLogViewSet)

urlpatterns = [
    path('api-token-auth/', views.obtain_auth_token),
    path('products/', product_list, name='product_list'),
    path('products/add/', product_create, name='product_add'),
    path('products/edit/<int:pk>/', product_update, name='product_edit'),
    path('products/delete/<int:pk>/', product_delete, name='product_delete'),
    path('products/add_stock/<int:pk>/', add_stock, name='add_stock'),
    path('products/remove_stock/<int:pk>/', remove_stock, name='remove_stock'),
    path('report/', report, name='report'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('register/', register, name='register'),
    path('api/', include(router.urls)),  
]

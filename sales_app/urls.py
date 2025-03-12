from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('employees/', views.employee_list, name='employee_list'),
    path('products/', views.product_list, name='product_list'),
    path('sales/', views.sales_list, name='sales_list'),
    path('add_sale/', views.add_sale, name='add_sale'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('daily_stats/', views.daily_stats, name='daily_stats'),
]
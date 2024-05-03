"""
URL configuration for Vendor_Management_System project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Vendor_Management import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('vendors/', views.get_vendor_list, name='vendor-list'),
    path('vendors/create/', views.create_vendor, name='create-vendor'),
    path('vendors/<int:pk>/', views.get_vendor_detail, name='vendor-detail'),
    path('vendors/<int:pk>/update/', views.update_vendor, name='update-vendor'),
    path('vendors/<int:pk>/delete/', views.delete_vendor, name='delete-vendor'),
    path('purchase_orders/', views.create_purchase_order, name='create-purchase-order'),
    path('purchase_order/', views.list_purchase_orders, name='list-purchase-orders'),
    path('purchase_orders/<int:po_id>/', views.get_purchase_order_detail, name='purchase-order-detail'),
    path('purchase_orders/<int:po_id>/update/', views.update_purchase_order, name='update-purchase-order'),
    path('purchase_orders/<int:po_id>/delete/', views.delete_purchase_order, name='delete-purchase-order'),
    path('vendors/<int:vendor_id>/performance/', views.get_vendor_performance, name='get-vendor-performance'),
]


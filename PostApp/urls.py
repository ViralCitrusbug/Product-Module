from django.contrib import admin
from django.urls import path
from .views import ProductListView, ProductDetail

urlpatterns = [
    path("products", ProductListView.as_view(), name="CRUD"),
    path("products/<pk>",ProductDetail.as_view(), name="product-detail")
]

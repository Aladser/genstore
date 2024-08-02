from django.urls import path
from product.views import *
from product.apps import ProductConfig

app_name = ProductConfig.name

urlpatterns = [
    path('', ProductListView.as_view(), name='list'),
    path('detail/<int:pk>',ProductDetailView.as_view(), name='detail'),
    path('create/', ProductCreateView.as_view(), name='create'),
    path('edit/<int:pk>', ProductUpdateView.as_view(), name='edit'),
    path('product/delete/<int:pk>', ProductDeleteView.as_view(), name='delete'),
]

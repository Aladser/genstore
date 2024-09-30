from django.urls import path

from blog.apps import BlogConfig
from blog.views import *

app_name = BlogConfig.name

urlpatterns = [
    path('', BlogListView.as_view(), name='list'),
    path('create/', BlogCreateView.as_view(), name='create'),
    path('detail/<int:pk>', BlogDetailView.as_view(), name='detail'),
    path('edit/<int:pk>', BlogUpdateView.as_view(), name='edit'),
    path('delete/<int:pk>', BlogDeleteView.as_view(), name='delete'),
    path('publish/', blog_publish, name="blog_publish")
]

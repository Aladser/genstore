from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from product.views import ProductListView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', ProductListView.as_view(), name='product_list'),

    path('user/', include('authen.urls', namespace='authen')),
    path('product/', include('product.urls', namespace='product')),
    path('blog/', include('blog.urls', namespace='blog'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

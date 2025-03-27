from django.conf.urls.static import static
from django.urls import path

from playersclub import settings
from .views import ShopView

urlpatterns = [
    path('shop/', ShopView.as_view(), name='shop'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

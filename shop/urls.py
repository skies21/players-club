from django.conf.urls.static import static
from django.urls import path

from playersclub import settings
from . import views

urlpatterns = [
    path('shop/', views.ShopView.as_view(), name='shop'),
    path('product/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),

    path('matches/', views.match_schedule, name='match_schedule'),
    path('add_match/', views.add_match, name='add_match'),
    path('edit_match/<int:match_id>/', views.edit_match, name='edit_match'),
    path('delete_match/<int:match_id>/', views.delete_match, name='delete_match'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

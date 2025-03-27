from django.views.generic import ListView
from .models import Product

class ShopView(ListView):
    model = Product
    template_name = 'shop/shop.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.filter(is_available=True)

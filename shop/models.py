from PIL import Image
from django.db import models

from users.models import CustomUser


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название")
    description = models.TextField(blank=True, verbose_name="Описание")
    price = models.IntegerField(verbose_name="Цена")
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name="Изображение")
    is_available = models.BooleanField(default=True, verbose_name="В наличии")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)
        img = img.resize((300, 400))
        img.save(self.image.path)


class CartItem(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    size = models.CharField(max_length=5, choices=[('S', 'S'), ('M', 'M'), ('L', 'L'), ('XL', 'XL')])

    def total_price(self):
        return self.quantity * self.product.price


class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    items = models.ManyToManyField(CartItem)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    delivery_method = models.CharField(max_length=50, choices=[('pickup', 'Самовывоз'), ('delivery', 'Доставка')])
    address = models.TextField(blank=True, null=True)
    payment_method = models.CharField(max_length=50, choices=[('sbp', 'СБП'), ('sber', 'Sber Pay'), ('card', 'Банковская карта')])
    created_at = models.DateTimeField(auto_now_add=True)

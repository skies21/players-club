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
    total_price = models.IntegerField()
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    delivery_method = models.CharField(max_length=50, choices=[('pickup', 'Самовывоз'), ('delivery', 'Доставка')])
    address = models.TextField(blank=True, null=True)
    payment_method = models.CharField(max_length=50, choices=[('sbp', 'СБП'), ('sber', 'Sber Pay'), ('card', 'Банковская карта')])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Заказ #{self.pk} от {self.full_name}"


class OrderedItem(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='ordered_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    size = models.CharField(max_length=5, choices=[('S', 'S'), ('M', 'M'), ('L', 'L'), ('XL', 'XL')])
    price = models.IntegerField()

    def total_price(self):
        return self.quantity * self.price


class Match(models.Model):
    team1 = models.CharField(max_length=100, verbose_name='Команда 1')
    team2 = models.CharField(max_length=100, verbose_name='Команда 2')
    match_date = models.DateTimeField(verbose_name='Дата и время матча')

    def __str__(self):
        return f'{self.team1} vs {self.team2} - {self.match_date}'


class Sector(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='sectors')
    name = models.CharField(max_length=100, verbose_name="Название сектора")
    image = models.ImageField(upload_to='sectors/', null=True, blank=True, verbose_name="Изображение сектора")
    price = models.IntegerField(verbose_name="Цена билета")
    rows = models.PositiveIntegerField(default=10, verbose_name="Количество рядов")
    seats_per_row = models.PositiveIntegerField(default=10, verbose_name="Мест в ряду")

    def __str__(self):
        return f"{self.name} — {self.match}"


class SeatReservation(models.Model):
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE, related_name='reservations')
    row_number = models.PositiveIntegerField(verbose_name="Ряд")
    seat_number = models.PositiveIntegerField(verbose_name="Место в ряду")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    reserved_at = models.DateTimeField(auto_now_add=True)
    order = models.ForeignKey(Order, null=True, blank=True, on_delete=models.SET_NULL, related_name='seats')

    class Meta:
        unique_together = ('sector', 'row_number', 'seat_number')

    def __str__(self):
        return f"Ряд {self.row_number}, место {self.seat_number} — {self.user} — {self.sector}"

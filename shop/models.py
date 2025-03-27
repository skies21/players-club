from PIL import Image
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название")
    description = models.TextField(blank=True, verbose_name="Описание")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name="Изображение")
    is_available = models.BooleanField(default=True, verbose_name="В наличии")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)
        img = img.resize((300, 400))
        img.save(self.image.path)

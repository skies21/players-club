# Generated by Django 5.1.7 on 2025-04-05 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_seatreservation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sector',
            name='price',
            field=models.IntegerField(verbose_name='Цена билета'),
        ),
    ]

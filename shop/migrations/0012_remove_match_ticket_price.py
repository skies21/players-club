# Generated by Django 5.1.7 on 2025-04-07 16:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0011_remove_order_items'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='match',
            name='ticket_price',
        ),
    ]

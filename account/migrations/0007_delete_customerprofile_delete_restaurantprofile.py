# Generated by Django 5.0.3 on 2024-04-06 12:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_remove_customerprofile_customer_id_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CustomerProfile',
        ),
        migrations.DeleteModel(
            name='RestaurantProfile',
        ),
    ]

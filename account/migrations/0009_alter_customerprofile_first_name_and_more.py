# Generated by Django 5.0.3 on 2024-04-14 01:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_customerprofile_restaurantprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customerprofile',
            name='first_name',
            field=models.CharField(default='frst name', max_length=255),
        ),
        migrations.AlterField(
            model_name='customerprofile',
            name='last_name',
            field=models.CharField(default='last name', max_length=255),
        ),
        migrations.AlterField(
            model_name='restaurantprofile',
            name='restaurant_name',
            field=models.CharField(default='Default Restaurant', max_length=255),
        ),
    ]
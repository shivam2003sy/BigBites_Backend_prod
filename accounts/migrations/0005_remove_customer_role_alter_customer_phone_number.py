# Generated by Django 5.0.6 on 2024-05-11 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_restaurant_description_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='role',
        ),
        migrations.AlterField(
            model_name='customer',
            name='phone_number',
            field=models.CharField(max_length=20),
        ),
    ]

# Generated by Django 5.0.6 on 2024-05-12 07:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='menuitem',
            old_name='restaurant',
            new_name='restaurant_Id',
        ),
    ]

# Generated by Django 5.0.6 on 2024-05-12 06:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_alter_restaurantverified_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurantverified',
            name='status',
            field=models.CharField(choices=[('initiated', 'Initiated'), ('approved', 'Approved'), ('rejected', 'Rejected'), ('pending', 'Pending')], default='initiated', max_length=50),
        ),
    ]

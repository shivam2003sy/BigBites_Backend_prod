# Generated by Django 5.0.6 on 2024-05-12 06:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0009_alter_restaurantverified_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='MenuItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('price', models.FloatField()),
                ('offer_price', models.FloatField(default=0.0)),
                ('image_url', models.URLField(blank=True, null=True)),
                ('categories', models.JSONField(default=list)),
                ('is_available', models.BooleanField(default=True)),
                ('time_to_prepare', models.IntegerField(default=0)),
                ('customization_options', models.JSONField(default=dict)),
                ('addition_prices', models.JSONField(default=dict)),
                ('nutritional_info', models.JSONField(default=dict)),
                ('allergens', models.JSONField(default=list)),
                ('removable_ingredients', models.JSONField(default=list)),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.restaurant')),
            ],
        ),
        migrations.CreateModel(
            name='MenuItemUserSelection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('selected_customizations', models.JSONField()),
                ('selected_additions', models.JSONField(default=dict)),
                ('removed_ingredients', models.JSONField(default=list)),
                ('quantity', models.IntegerField(default=1)),
                ('menu_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restaurant.menuitem')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.customer')),
            ],
        ),
    ]
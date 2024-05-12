from django.db import models

from accounts.models import Restaurant , Customer

class MenuItem(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.FloatField()
    offer_price = models.FloatField(default=0.0)
    image_url = models.URLField(blank=True, null=True)
    categories = models.JSONField(default=list)
    is_available = models.BooleanField(default=True)
    time_to_prepare = models.IntegerField(default=0)
    customization_options = models.JSONField(default=dict)
    addition_prices = models.JSONField(default=dict)
    nutritional_info = models.JSONField(default=dict)
    allergens = models.JSONField(default=list)
    removable_ingredients = models.JSONField(default=list)

    def __str__(self):
        return self.name

class MenuItemUserSelection(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    selected_customizations = models.JSONField()
    selected_additions = models.JSONField(default=dict)
    removed_ingredients = models.JSONField(default=list)
    quantity = models.IntegerField(default=1)
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.menu_item.name} - {self.user.name}"












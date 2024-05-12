from django.contrib import admin

# Register your models here.

from .models import User, Customer, Restaurant , RestaurantVerified


# Register your models here and add them to the admin panel here
admin.site.register(User)
admin.site.register(Customer)
admin.site.register(Restaurant)
admin.site.register(RestaurantVerified)








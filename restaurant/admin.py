from django.contrib import admin

# Register your models here.


from .models import MenuItem, MenuItemUserSelection

admin.site.register(MenuItem)
admin.site.register(MenuItemUserSelection)
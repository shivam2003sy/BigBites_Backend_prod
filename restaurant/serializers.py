# Path: restaurant/serializers.py
from rest_framework import serializers
from .models import MenuItem, MenuItemUserSelection
from accounts.serializers import RestaurantSerializer, CustomerSerializer
class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = '__all__'

class MenuItemUserSelectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItemUserSelection
        fields = '__all__'


class MenuItemUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = '__all__'
        read_only_fields = ['restaurant']
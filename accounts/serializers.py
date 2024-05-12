# accounts/serializers.py
from rest_framework import serializers
from .models import User, Customer, Restaurant,  RestaurantVerified



class RestaurantVerifiedSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantVerified
        fields = '__all__'
        
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = '__all__'
        def create(self, validated_data):
            password = validated_data.pop('password', None)
            instance = self.Meta.model(**validated_data)
            if password is not None:
                instance.set_password(password)
            instance.save()
            return instance
        def update(self, instance, validated_data):
            password = validated_data.pop("password", None)
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
                if instance.password is not None:
                    instance.set_password(password)
            instance.save()
            return instance            


class CustomerSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Customer
        fields = '__all__'

class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = '__all__'
class UserUpdateSerializer(serializers.ModelSerializer):   
    class Meta:
        model = User
        fields = '__all__'
        read_only_fields = ['id', 'email', 'firebase_uid' , 'first_name', 'last_name' , 'password', 'user_type']


class RestaurantUpdateSerializer(serializers.ModelSerializer):
      
    class Meta:
        model = Restaurant
        fields = '__all__'
        read_only_fields = ['id', 'email', 'firebase_uid' , 'first_name', 'last_name' , 'password', 'user_type']



from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response 
from django.shortcuts import get_object_or_404
from .models import MenuItem, MenuItemUserSelection
from .serializers import MenuItemSerializer, MenuItemUserSelectionSerializer, MenuItemUpdateSerializer
from accounts.models import Restaurant
from accounts.serializers import RestaurantSerializer
from accounts.firebaseauth.firebase_authentication import FirebaseAuthentication

class MenuItemViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [FirebaseAuthentication]

    def list(self, request):
        restaurant = request.user
        queryset = MenuItem.objects.filter(restaurant=restaurant)
        serializer = MenuItemSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        restaurant = request.user
        queryset = get_object_or_404(MenuItem, restaurant=restaurant, id=pk)
        serializer = MenuItemSerializer(queryset)
        return Response(serializer.data)

    def create(self, request):
        restaurant =  Restaurant.objects.get(id=request.user.id)
        request.data['restaurant'] = restaurant.pk
        serializer = MenuItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        menu_item = get_object_or_404(MenuItem, pk=pk)
        serializer = MenuItemUpdateSerializer(menu_item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'Menu item updated', 'data': serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        menu_item =MenuItem.objects.get(id=pk)
        if menu_item:
            menu_item.delete()
            return Response({'status': 'Menu item deleted'})
        return Response({'status': 'Menu item not found'}, status=status.HTTP_404_NOT_FOUND)
    

class MenuItemUserSelectionViewSet(viewsets.ModelViewSet):
    queryset = MenuItemUserSelection.objects.all()
    serializer_class = MenuItemUserSelectionSerializer

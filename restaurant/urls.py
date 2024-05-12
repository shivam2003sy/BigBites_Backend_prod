from django.urls import path
from .views import MenuItemViewSet, MenuItemUserSelectionViewSet

urlpatterns = [
    path('menuitem/', MenuItemViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('menuitem/<int:pk>/', MenuItemViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('menuitemuserselection/', MenuItemUserSelectionViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('menuitemuserselection/<int:pk>/', MenuItemUserSelectionViewSet.as_view({'get': 'retrieve', 'put': 'update'}))
]

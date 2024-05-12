# accounts/urls.py
from django.urls import path
from .views import AuthCreateNewUserView, AuthLoginUserView , UserPasswordResetView , RetrieveUpdateDestroyExistingUser 


urlpatterns = [
    path('signup/', AuthCreateNewUserView.as_view(), name='auth-signup'),
    path('login/', AuthLoginUserView.as_view(), name='auth-login'),    
    path('', RetrieveUpdateDestroyExistingUser.as_view(), name='retrieve-update-user'),
    path('reset-password/', UserPasswordResetView.as_view(), name='user-reset-password'),
]
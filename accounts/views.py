# accounts/views.py
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import User, Customer, Restaurant,  RestaurantVerified
from .serializers import UserSerializer, CustomerSerializer, RestaurantSerializer,  UserUpdateSerializer ,  RestaurantUpdateSerializer , RestaurantVerifiedSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.permissions import AllowAny
from .firebaseauth.firebase_authentication import FirebaseAuthentication
from firebase_admin import auth as firebase_admin_auth
from django.contrib.auth.hashers import check_password
import re
from big_bites.settings import auth

from  accounts.utils.email_varification import generate_custom_email_from_firebase
from accounts.utils.custom_password_reset_link import generate_custom_password_link_from_firebase
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound, ValidationError
class AuthCreateNewUserView(APIView):
    
    """
    Create a new user by providing the type of user, email and password.
    """

    permission_classes = [AllowAny]
    authentication_classes = []
    def post(self, request: Request, format=None):
        print("request.data", request.data)
        data  =  request.data
        email = data.get('email').strip().lower()
        password = data.get('password')
        user_type = data.get('user_type')
        if not email:
            return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)
        if not password:
            return Response({'error': 'Password is required'}, status=status.HTTP_400_BAD_REQUEST)
        if not user_type:
            return Response({'error': 'User type is required'}, status=status.HTTP_400_BAD_REQUEST)
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return Response({'error': 'Invalid email address'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = auth.create_user_with_email_and_password(email, password)
            user_id = user['localId']
            data['firebase_uid'] = user_id
            data['is_active'] = True
            try:
                display_name = email.split('@')[0]
                generate_custom_email_from_firebase(email, display_name)
            except Exception as e:
                # delete firebase user if user creation fails
                firebase_admin_auth.delete_user(user_id)
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
            if user_type == 'customer':
                serializer = CustomerSerializer(data=data)
            elif user_type == 'restaurant':
                # crete a restaurant Verified object
                restaurant_verified = RestaurantVerified.objects.create()
                data['varified_restaurant'] = restaurant_verified.id
                serializer = RestaurantSerializer(data=data)
            if serializer.is_valid():                
                serializer.save()
                return Response({
                    'message': 'User created successfully',
                    'data': serializer.data
                }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AuthLoginUserView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    @swagger_auto_schema(
            operation_summary="Login a user",
            operation_description="Login a user by providing the email and password.",
            tags=["User Management"],
            request_body=UserSerializer,
            responses={200: UserSerializer(many=False), 400: "User login failed."}
            )
    def post(self, request: Request, format=None):
        data = request.data
        email = data.get('email')
        password = data.get('password')
        if not email:
            return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)
        if not password:
            return Response({'error': 'Password is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = auth.sign_in_with_email_and_password(email, password)
        except Exception as e:
            return Response({'error': 'Invalid email or password'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            existing_user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'Invalid email or password'}, status=status.HTTP_400_BAD_REQUEST)
        if existing_user:
            serializer = UserSerializer(existing_user)
            extra_data = {
                "firebase_id" : user['localId'],
                "firebase_access_tocken" : user['idToken'],
                'firebase_refresh_token' : user['refreshToken'],
                'firebase_expires_in' : user['expiresIn'],
                'firebase_kind' : user['kind'],
                "user_data": serializer.data
            }
            return Response({
                'message': 'User logged in successfully',
                'data': extra_data
            }, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid email or password'}, status=status.HTTP_400_BAD_REQUEST)
    

    



class RetrieveUpdateDestroyExistingUser(APIView):
    """
    API endpoint to retrieve, update, or delete an existing user.
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [FirebaseAuthentication]

    def get(self, request: Request):
        try:
            user =  request.user
            user = User.objects.get(firebase_uid=user.firebase_uid)
            if user.user_type == 'customer':
                serializer = CustomerSerializer(user)
            elif user.user_type == 'restaurant':
                serializer = RestaurantUpdateSerializer(user)
                resturant = Restaurant.objects.get(email = user)
                serializer_restaurant = RestaurantVerifiedSerializer(resturant.varified_restaurant)
            response = {
                "status": "success",
                "data": serializer.data,
                "varified_restaurant": serializer_restaurant.data
            }
            return Response(response, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            bad_response = {
                "status": "failed",
                "message": "User does not exist."
            }
            return Response(bad_response, status=status.HTTP_404_NOT_FOUND)
        except Exception:
            bad_response = {
                "status": "failed",
                "message": "User does not exist."
            }
            return Response(bad_response, status=status.HTTP_400_BAD_REQUEST)
        

    def patch(self, request: Request):
        data = request.data
        try:
            user = request.user
            # Checking if the user exists based on both id and firebase_uid
            user = User.objects.get(id=user.id, firebase_uid=user.firebase_uid)
        except User.DoesNotExist:
            # Handling the case where the user does not exist
            raise NotFound("User does not exist.")
        # Catching specific ValidationError raised by the serializer
        except ValidationError as e:
            bad_response = {
                "status": "failed",
                "message": "Invalid data provided.",
                "data": e.detail  # Including the detailed validation errors in the response
            }
            return Response(bad_response, status=status.HTTP_400_BAD_REQUEST)

        # Check if any keys in data are not allowed to be updated
        invalid_keys = [key for key in data.keys() if key not in ['first_name', 'last_name', 'email', 'password']]
        if invalid_keys == []:
            bad_response = {
                "status": "failed",
                "message": f" 'first_name', 'last_name', 'email', 'password' are not  allowed to be updated. Invalid keys: {invalid_keys}"
            }
            return Response(bad_response, status=status.HTTP_400_BAD_REQUEST)

        if user.user_type == 'customer':
            serializer = UserUpdateSerializer(user, data=data, partial=True)
        elif user.user_type == 'restaurant':
            serializer = RestaurantUpdateSerializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            resturant = Restaurant.objects.get(email = user)
            # change the status of the restaurant to pending
            verified_restaurant = RestaurantVerified.objects.get(id=resturant.varified_restaurant.id)
            verified_restaurant.status = "pending"
            verified_restaurant.save()
            serializer_restaurant = RestaurantVerifiedSerializer(verified_restaurant)
            response = {
                "status": "success",
                "message": "User updated successfully.",
                "data": serializer.data,
                "varified_restaurant": serializer_restaurant.data
            }
            return Response(response, status=status.HTTP_200_OK)
        else:
            bad_response = {
                "status": "failed",
                "message": "User update failed.",
                "data": serializer.errors
            }
            return Response(bad_response, status=status.HTTP_400_BAD_REQUEST)
            
        
    def delete(self, request: Request):
        try:
            user =  request.user
            user = User.objects.get(id=user.id , firebase_uid=user.firebase_uid)
            try:
                firebase_admin_auth.delete_user(user.firebase_uid)
            except Exception:
                bad_response = {
                    "status": "failed",
                    "message": "User does not exist on firebase."
                }
                return Response(bad_response, status=status.HTTP_404_NOT_FOUND)
            user.delete()
            
            response = {
                "status": "success",
                "message": "User deleted successfully."
            }
            return Response(response, status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            bad_response = {
                "status": "failed",
                "message": "User does not exist."
            }
            return Response(bad_response, status=status.HTTP_404_NOT_FOUND)
        except Exception:
            bad_response = {
                "status": "failed",
                "message": "User does not exist."
            }
            return Response(bad_response, status=status.HTTP_400_BAD_REQUEST)
        

class UserPasswordResetView(APIView):
    """
    API endpoint to reset an existing drive user's password.
    """
    permission_classes = [AllowAny]
    authentication_classes = []
    def get(self, request: Request):
        email = request.query_params.get('email').strip().lower()
        if email and not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            bad_response = {
                "status": "failed",
                "message": "Enter a valid email address."
            }
            return Response(bad_response, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(email=email)
            first_name = user.first_name
            # sending custom password reset link
            try:
                user_email = email
                display_name = email.split('@')[0]
                generate_custom_password_link_from_firebase(user_email, display_name)
                response = {
                    "status": "success",
                    "message": "Password reset link sent successfully.",
                }
                return Response(response, status=status.HTTP_200_OK)
            except Exception:
                bad_response = {
                    "status": "failed",
                    "message": "Password reset link could not be sent; Please try again."
                }
                return Response(bad_response, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            bad_response = {
                "status": "failed",
                "message": "User does not exist."
            }
            return Response(bad_response, status=status.HTTP_404_NOT_FOUND)

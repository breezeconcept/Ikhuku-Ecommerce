from rest_framework import generics, status
from rest_framework.response import Response
from .models import CustomUser, SellerProfile
from .serializers import ( 
    CreateUserSerializer, 
    UpdateUserSerializer, 
    EmailVerificationSerializer, 
    SellerProfileSerializer,
    SellerVerificationSerializer,
    ResetPasswordSerializer, ResetPasswordConfirmSerializer
    )
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import AllowAny
from django.core.mail import send_mail
from .permissions import IsSuperUserOrReadOnly, IsAdmin
from django.conf import settings

# from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from .utils import get_user_id_from_jwt, CustomRenderer




# Endpoint to register a user
class CreateUserView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CreateUserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(self.request.data.get('password'))
        user.save()


# Endpoint to verify a user's email
class EmailVerificationView(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = EmailVerificationSerializer  # Create serializer for verification
    lookup_field = 'id'

    def put(self, request, id):
        user = self.get_object()
        user.is_verified = True
        user.is_active = True
        user.save()
        return Response({'message': 'Email verified successfully'}, status=status.HTTP_200_OK)


# Endpoint to update other user's information
class UpdateUserView(generics.RetrieveUpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UpdateUserSerializer
    permission_classes = [IsAuthenticated]
    renderer_classes = [CustomRenderer]

    def get_object(self):
        user_id = get_user_id_from_jwt(self.request)
        if user_id:
            # Fetch the user object using the user_id obtained from the token
            try:
                user = CustomUser.objects.get(id=user_id)
                return user
            except CustomUser.DoesNotExist:
                return None
        else:
            return None




# Endpoint to login a user
class UserLoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(request, email=email, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh),
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
# class UserLoginView(APIView):
#     def post(self, request):
#         email = request.data.get('email')
#         password = request.data.get('password')

#         user = authenticate(request, email=email, password=password)
#         if user:
#             token, created = Token.objects.get_or_create(user=user)
#             return Response({'token': token.key}, status=status.HTTP_200_OK)
#         else:
#             return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        



# class TokenRefreshView(APIView):
#     def post(self, request):
#         refresh_token = request.data.get('refresh')
        
#         if not refresh_token:
#             return Response({'error': 'Refresh token not provided'}, status=status.HTTP_400_BAD_REQUEST)
        
#         try:
#             refresh = RefreshToken(refresh_token)
#             access_token = str(refresh.access_token)
#             return Response({'access_token': access_token}, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({'error': 'Invalid refresh token'}, status=status.HTTP_400_BAD_REQUEST)



# class TokenVerifyView(APIView):
#     def post(self, request):
#         token = request.data.get('token')
        
#         if not token:
#             return Response({'error': 'Token not provided'}, status=status.HTTP_400_BAD_REQUEST)
        
#         try:
#             access_token = AccessToken(token)
#             if access_token.is_valid():
#                 return Response({'message': 'Token is valid'}, status=status.HTTP_200_OK)
#             else:
#                 return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
#         except Exception as e:
#             return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)




class PasswordResetRequestView(APIView):
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = CustomUser.objects.filter(email=email).first()

            if user:
                # Generate password reset token
                token_generator = PasswordResetTokenGenerator()
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = token_generator.make_token(user)

                reset_url = reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
                reset_link = request.build_absolute_uri(reset_url)

                send_mail(
                    'Password Reset Request',
                    f'Click the link to reset your password: {reset_link}',
                    f'{settings.DEFAULT_FROM_EMAIL}',
                    [email],
                    fail_silently=False,
                )

                return Response({'message': 'Password reset email sent'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


UserModel = get_user_model()

class PasswordResetConfirmView(generics.CreateAPIView):
    serializer_class = ResetPasswordConfirmSerializer
    def post(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = UserModel.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
            user = None

        if user and PasswordResetTokenGenerator().check_token(user, token):
            # Handle the password reset logic here
            # Example: Reset the user's password
            new_password = request.data.get('password')

            if new_password:
                user.set_password(new_password)
                user.save()
                return Response({'message': 'Password reset successful'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'New password is required'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Invalid token or user'}, status=status.HTTP_400_BAD_REQUEST)





# from django.contrib.auth.tokens import PasswordResetTokenGenerator
# from django.contrib.auth import get_user_model
# from django.utils.encoding import force_str
# from django.utils.http import urlsafe_base64_decode
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework import serializers

# UserModel = get_user_model()

# class PasswordResetConfirmView(APIView):
#     def post(self, request, uidb64, token):
#         try:
#             uid = force_str(urlsafe_base64_decode(uidb64))
#             user = UserModel.objects.get(pk=uid)
#         except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
#             user = None

#         if user and PasswordResetTokenGenerator().check_token(user, token):
#             new_password = request.data.get('password')

#             if new_password:
#                 user.set_password(new_password)
#                 user.save()
#                 return Response({'message': 'Password reset successful'}, status=status.HTTP_200_OK)
#             else:
#                 return Response({'error': 'New password is required'}, status=status.HTTP_400_BAD_REQUEST)
#         else:
#             return Response({'error': 'Invalid token or user'}, status=status.HTTP_400_BAD_REQUEST)

# class ResetPasswordConfirmSerializer(serializers.Serializer):
#     password = serializers.CharField()






# Endpoint to logout a user
# class UserLogoutView(APIView):
#     permission_classes = (IsAuthenticated,)

#     def post(self, request):
#         try:
#             # Get the user's token and delete it
#             token = Token.objects.get(user=request.user)
#             token.delete()
#             return Response({"message": "Logout successful."}, status=status.HTTP_200_OK)
#         except Token.DoesNotExist:
#             return Response({"error": "User is not logged in."}, status=status.HTTP_400_BAD_REQUEST)
#         except Exception as e:
#             return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        current_password = request.data.get('current_password')
        new_password = request.data.get('new_password')

        if user.check_password(current_password):
            if new_password:
                user.set_password(new_password)
                user.save()
                return Response({'message': 'Password changed successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'New password is required'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Current password is incorrect'}, status=status.HTTP_400_BAD_REQUEST)



# Endpoint to create a seller profile
class SellerProfileCreateView(generics.CreateAPIView):
    serializer_class = SellerProfileSerializer
    permission_classes = [IsAuthenticated]
    # renderer_classes = [CustomRenderer]


    def post(self, request, *args, **kwargs):
        user = self.request.user

        # Check if a seller profile already exists for the user
        if SellerProfile.objects.filter(user=user).exists():
            message = 'Seller profile already exists for this user'
            response_data = {
                "message": message,
                "status": status.HTTP_400_BAD_REQUEST,
                "data": {
                    "error_details": "You cannot create multiple seller profiles for the same user."
                }
            }
            return Response(response_data)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user)

        user.is_merchant = True
        user.save()

        # Retrieve the created seller profile instance
        seller_profile_instance = serializer.instance
        seller_profile_data = serializer.data

        formatted_data = "\n".join([f"{field}: {seller_profile_data.get(field)}" for field in seller_profile_data])

        # Send email with seller profile data to the company
        email_subject = 'New Seller Profile Submission'
        email_body = f"A new seller profile has been submitted by {user.email}.\n\nSeller Profile Data:\n{seller_profile_instance}\n\n{formatted_data}\n\nPlease review and verify the seller."
        sender_email = user.email  # Use the user's email
        receiver_email = settings.DEFAULT_FROM_EMAIL
        
        email_subject2 = 'Seller Profile Recieved'
        email_body2 = f"Hello {user.first_name} {user.last_name},\nYour seller profile has been received and it's being reviewed by the team.\nThis review process could last for 3 to 5 working days, Pls exercise patience.\nKeep an eye on your inbox, you will recieve an email once we verify you.\n And if your profile didn't pass the checks, you would also get an email indicating the reason."
        sender_email2 = settings.DEFAULT_FROM_EMAIL  # Use the user's email
        receiver_email2 = user.email

        try:
            send_mail(email_subject, email_body, sender_email, [receiver_email], fail_silently=False)
            send_mail(email_subject2, email_body2, sender_email2, [receiver_email2], fail_silently=False)
            message = 'Seller profile created successfully'
            response_data = {
                "message": message,
                "status": status.HTTP_201_CREATED,
                "data": seller_profile_data
            }
            return Response(response_data)
        except Exception as e:
            message = 'Email unsuccessful'
            response_data = {
                "message": message,
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "data": {
                    "error_details": "Failed to send email."
                }
            }
            return Response(response_data)




# Endpoint to verify a seller profile
class SellerVerificationView(generics.UpdateAPIView):
    serializer_class = SellerVerificationSerializer  # Serializer for seller verification
    permission_classes = [IsAdmin]  # Admin permission required for verification
    queryset = SellerProfile.objects.all()  # Queryset to get SellerProfile instances
    lookup_field = 'id'  # Field to lookup seller profile by ID

    def update(self, request, *args, **kwargs):
        seller_profile = self.get_object()  # Retrieve the seller profile instance
        serializer = self.get_serializer(seller_profile, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(is_verified=True)  # Set the seller profile as verified

        # Notify the seller via email or other means
        email_subject = 'Seller Profile Verified'
        email_body = f"Your seller profile with ID: {seller_profile.id} has been verified."
        receiver_email = seller_profile.user.email  # Use the user's email

        try:
            send_mail(email_subject, email_body, settings.DEFAULT_FROM_EMAIL, [receiver_email], fail_silently=False)
        except Exception as e:
            # Handle email sending error (optional)
            pass

        return Response({'message': 'Seller profile verified successfully'}, status=status.HTTP_200_OK)
    


class SellerProfileRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = SellerProfileSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        seller_profile = self.get_object()
        serializer = self.get_serializer(seller_profile)
        return Response(serializer.data)

    def get_object(self):
        # Retrieve the authenticated user
        user = self.request.user

        # Get the seller profile instance related to the user
        try:
            seller_profile = SellerProfile.objects.get(user=user)
            self.check_object_permissions(self.request, seller_profile)
            return seller_profile
        except SellerProfile.DoesNotExist:
            # If the seller profile doesn't exist, return an appropriate response
            return Response("Seller profile does not exist for this user.", status=status.HTTP_404_NOT_FOUND)
    


# class SellerProfileRetrieveDestroyView(generics.RetrieveDestroyAPIView):
#     serializer_class = SellerProfileSerializer
#     permission_classes = [IsAuthenticated]

#     def get_object(self):
#         # Retrieve the authenticated user
#         user = self.request.user

#         # Get the seller profile instance related to the user
#         try:
#             seller_profile = SellerProfile.objects.get(user=user)
#             self.check_object_permissions(self.request, seller_profile)
#             return seller_profile
#         except SellerProfile.DoesNotExist:
#             # If the seller profile doesn't exist, return 404 Not Found
#             return Response("Seller profile does not exist for this user.")




# Endpoint to give an account staff rights
class GrantStaffRightsView(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CreateUserSerializer
    permission_classes = [IsAuthenticated, IsSuperUserOrReadOnly]
    lookup_field = 'id'

    def put(self, request, *args, **kwargs):
        user = self.get_object()
        user.is_staff = True
        user.is_admin = True
        user.save()
        return Response({'message': 'Admin rights granted successfully'}, status=status.HTTP_200_OK)


# Endpoint to revoke staff rights from an account
class RevokeStaffRightsView(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CreateUserSerializer
    permission_classes = [IsAuthenticated, IsSuperUserOrReadOnly]
    lookup_field = 'id'

    def put(self, request, *args, **kwargs):
        user = self.get_object()
        user.is_staff = False
        user.is_admin = False
        user.save()
        return Response({'message': 'Admin rights revoked successfully'}, status=status.HTTP_200_OK)
    

# Endpoint to give an account admin rights
class GrantAdminRightsView(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CreateUserSerializer
    permission_classes = [IsAdminUser]
    lookup_field = 'id'

    def put(self, request, *args, **kwargs):
        user = self.get_object()
        user.is_admin = True
        user.save()
        return Response({'message': 'Admin rights granted successfully'}, status=status.HTTP_200_OK)

from drf_yasg.utils import swagger_auto_schema
# Endpoint to revoke admin rights from an account

class RevokeAdminRightsView(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CreateUserSerializer
    permission_classes = [IsAdminUser]
    lookup_field = 'id'

    # @swagger_auto_schema(tags=['revoke-admin-rights'], operation_summary="Your one-line description here")
    @swagger_auto_schema(operation_summary="Your one-line description here")
    def put(self, request, *args, **kwargs):
        user = self.get_object()
        user.is_admin = False
        user.save()
        return Response({'message': 'Admin rights revoked successfully'}, status=status.HTTP_200_OK)

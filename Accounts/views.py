from rest_framework import generics, status
from rest_framework.response import Response
from .models import CustomUser, SellerProfile
from .serializers import ( 
    CreateUserSerializer, 
    UpdateUserSerializer, 
    EmailVerificationSerializer, 
    SellerProfileSerializer,
    SellerVerificationSerializer,
    ResetPasswordSerializer 
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
from rest_framework_simplejwt.tokens import RefreshToken




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

    def get_object(self):
        return self.request.user  




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
        



class TokenRefreshView(APIView):
    def post(self, request):
        refresh_token = request.data.get('refresh')
        
        if not refresh_token:
            return Response({'error': 'Refresh token not provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)
            return Response({'access_token': access_token}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': 'Invalid refresh token'}, status=status.HTTP_400_BAD_REQUEST)



class TokenVerifyView(APIView):
    def post(self, request):
        token = request.data.get('token')
        
        if not token:
            return Response({'error': 'Token not provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            refresh = RefreshToken(str(token))  # Ensure the token is converted to a string
            refresh.check_blacklist()
            return Response({'message': 'Token is valid'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)




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

class PasswordResetConfirmView(APIView):
    def post(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = UserModel.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
            user = None

        if user and PasswordResetTokenGenerator().check_token(user, token):
            # Handle the password reset logic here
            # Example: Reset the user's password
            new_password = request.data.get('new_password')

            if new_password:
                user.set_password(new_password)
                user.save()
                return Response({'message': 'Password reset successful'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'New password is required'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Invalid token or user'}, status=status.HTTP_400_BAD_REQUEST)



# Endpoint to logout a user
class UserLogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            # Get the user's token and delete it
            token = Token.objects.get(user=request.user)
            token.delete()
            return Response({"message": "Logout successful."}, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            return Response({"error": "User is not logged in."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


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

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)
        user.is_merchant = True
        user.save()

        # Retrieve the created seller profile instance
        seller_profile_instance = serializer.instance

        # Send email with seller profile data to the company
        email_subject = 'New Seller Profile Submission'
        email_body = f"A new seller profile has been submitted by {user.email}.\n\nSeller Profile Data:\n{seller_profile_instance}\n\nPlease review and verify the seller."
        sender_email = f'{user.email}'  # Replace with your sender email
        receiver_email = f'{settings.DEFAULT_FROM_EMAIL}'   # Replace with company email

        try:
            send_mail(email_subject, email_body, sender_email, [receiver_email], fail_silently=False)
        except Exception as e:
            # Handle email sending error
            return Response({'error': 'Failed to send email'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'message': 'Seller profile created successfully'}, status=status.HTTP_201_CREATED)


# Endpoint to verify a seller profile
class SellerVerificationView(generics.UpdateAPIView):
    serializer_class = SellerVerificationSerializer
    permission_classes = [IsAdmin]
    queryset = CustomUser.objects.all()  # Define the queryset

    def update(self, request, *args, **kwargs):
        instance = self.get_object()  # Retrieve the instance to be updated
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # Custom logic after updating the instance
        user = get_object_or_404(CustomUser, pk=kwargs['seller_id'])
        user.is_verified = True
        user.save()

        # Retrieve the updated seller profile instance
        seller_profile_instance = serializer.instance

        # Send email with seller profile data to the company
        email_subject = 'Seller Profile Approval'
        email_body = f"Hello {user.email}, \nYour seller profile has been screened and approved, Happy sales!!!.\n\nSeller Profile Data:\n{seller_profile_instance}."
        sender_email = settings.DEFAULT_FROM_EMAIL  # Use settings directly
        receiver_email = user.email  # Use user's email for receiver

        try:
            send_mail(email_subject, email_body, sender_email, [receiver_email], fail_silently=False)
        except Exception as e:
            # Handle email sending error
            return Response({'error': 'Failed to send email'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'message': 'Seller has been verified'}, status=status.HTTP_200_OK)


# Endpoint to give an account staff rights
class GrantStaffRightsView(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CreateUserSerializer
    permission_classes = [IsAuthenticated, IsSuperUserOrReadOnly]

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

    def put(self, request, *args, **kwargs):
        user = self.get_object()
        user.is_admin = True
        user.save()
        return Response({'message': 'Admin rights granted successfully'}, status=status.HTTP_200_OK)


# Endpoint to revoke admin rights from an account
class RevokeAdminRightsView(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CreateUserSerializer
    permission_classes = [IsAdminUser]

    def put(self, request, *args, **kwargs):
        user = self.get_object()
        user.is_admin = False
        user.save()
        return Response({'message': 'Admin rights revoked successfully'}, status=status.HTTP_200_OK)

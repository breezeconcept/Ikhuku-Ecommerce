from rest_framework import serializers
from .models import CustomUser, SellerProfile





class CreateUserSerializer(serializers.ModelSerializer):
    profile_picture = serializers.ImageField(allow_null=True, required=False)
    address = serializers.CharField(allow_blank=True, required=False)


    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name', 'last_name', 'phone_number', 'profile_picture', 'address', 'password',  'is_merchant', 'is_verified']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        profile_picture = validated_data.pop('profile_picture', None)
        address = validated_data.pop('address', None)
        user = CustomUser.objects.create_user(**validated_data, profile_picture=profile_picture, address=address)
        if profile_picture:
            user.profile_picture = profile_picture
        if address:
            user.address = address
        user.save()
        return user
    




class EmailVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = []  # Empty fields as it's only for verification



class UpdateUserSerializer(serializers.ModelSerializer):
    profile_picture = serializers.ImageField(allow_null=True, required=False)
    address = serializers.CharField(allow_blank=True, required=False)

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'phone_number', 'profile_picture', 'address']



class SellerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellerProfile
        fields = '__all__'  # Include all fields in the serializer



class SellerVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellerProfile
        fields = ['is_verified']  # Fields that can be updated by admin for seller verification




class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    class Meta:
        model = CustomUser
        fields = ['email']


from rest_framework import serializers
from .models import CustomUser, SellerProfile





class CreateUserSerializer(serializers.ModelSerializer):
    # profile_picture = serializers.ImageField(allow_null=True, required=False)
    address = serializers.CharField(allow_blank=True, required=False)
    is_merchant = serializers.ReadOnlyField()
    is_verified = serializers.ReadOnlyField()


    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name', 'last_name', 'phone_number', 'address', 'password',  'is_merchant', 'is_verified']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # profile_picture = validated_data.pop('profile_picture', None)
        address = validated_data.pop('address', None)
        user = CustomUser.objects.create_user(**validated_data, address=address)
        # if profile_picture:
        #     user.profile_picture = profile_picture
        if address:
            user.address = address
        user.save()
        return user
    




class EmailVerificationSerializer(serializers.ModelSerializer):
    is_verified = serializers.ReadOnlyField()
    class Meta:
        model = CustomUser
        fields = ['is_verified']  # Empty fields as it's only for verification



class UpdateUserSerializer(serializers.ModelSerializer):
    # profile_picture = serializers.ImageField(allow_null=True, required=False)
    address = serializers.CharField(allow_blank=True, required=False)
    is_merchant = serializers.ReadOnlyField()
    is_verified = serializers.ReadOnlyField()

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'phone_number', 'address', 'is_merchant', 'is_verified']



class SellerProfileSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)  # Make user field read-only
    is_verified = serializers.ReadOnlyField()
    class Meta:
        model = SellerProfile
        fields = "__all__"


class SellerVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellerProfile
        fields = ['is_verified']  # Fields that can be updated by admin for seller verification




class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    class Meta:
        model = CustomUser
        fields = ['email']


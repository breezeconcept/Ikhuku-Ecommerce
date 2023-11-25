from rest_framework import serializers
from .models import CustomUser

from rest_framework import serializers
from .models import CustomUser



class CreateUserSerializer(serializers.ModelSerializer):
    profile_picture = serializers.ImageField(allow_null=True, required=False)
    address = serializers.CharField(allow_blank=True, required=False)


    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name', 'last_name', 'phone_number', 'profile_picture', 'address', 'password']
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
    



class UpdateUserSerializer(serializers.ModelSerializer):
    profile_picture = serializers.ImageField(allow_null=True, required=False)
    address = serializers.CharField(allow_blank=True, required=False)

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'phone_number', 'profile_picture', 'address']



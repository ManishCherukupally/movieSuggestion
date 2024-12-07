from rest_framework import serializers
from django.contrib.auth.models import User
from .models import User_details,Movies


class RegistrationSerializer(serializers.ModelSerializer):
    contact_no = serializers.CharField(required=True)
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name', 'contact_no']  # Use first_name instead of firstname
        extra_kwargs = {
            'password': {'write_only': True},  # Ensure password is not returned
        }
    def validate(self, data):
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError({'username': 'This_username_is_already_taken.'})
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({'email': 'This_email_was_already_existed'})
        if User_details.objects.filter(contact_no=data['contact_no']).exists():
            raise serializers.ValidationError({'contact_no': 'This_mobile_number_is_already_registered.'})

        return data

    def create(self, validated_data):
        contact_no = validated_data.pop('contact_no')

        # Create the User instance
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email'],
            first_name=validated_data.get('first_name',''),
            last_name=validated_data.get('last_name','')
        )

        # Create the UserDetails instance linked to the User
        User_details.objects.create(user_id=user, contact_no=contact_no)

        return user


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.CharField(error_messages={'blank': 'username_field_cannot_be_blank.'},required=True)

    password = serializers.CharField(error_messages={'blank': ' password_field_cannot_be_blank.'},required=True)



    class Meta:
        model = User
        fields = ['email','password']

class MovieSerializer(serializers.ModelSerializer):


    class Meta:
        model = Movies
        fields = '__all__'
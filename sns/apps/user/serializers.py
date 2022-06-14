from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from django.utils.translation import gettext as _

from .models import Group, GroupMembership

class UserSerializer(serializers.ModelSerializer):
    """Serializer for the users object"""

    class Meta:
        model = get_user_model()
        fields = ('email', 'name', 'mobile', 'address', 'city', 'pincode', 'password', 'is_staff')
        extra_kwargs = {
            'password': {
                'write_only': True, # password should only be for writing and should not be returned as a part of GET call
                'min_length': 5,
                'style': {'input_type': 'password'} # Styling to see * instead of seeing pwd characters
            }
        }

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update a user, setting password correctly and return it"""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for user authentication object"""
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        """Validate and authenticate users"""
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )
        if not user:
            msg = 'Unable to authenticate with provided credentials'
            raise serializers.ValidationError(msg, code='authentication')

        attrs['user'] = user
        return attrs


class GroupSerializer(serializers.ModelSerializer):
    """Serializer for the community group"""

    class Meta:
        model = Group
        fields = "__all__"
        read_only_fields = ('id',)


class GroupStatusSerializer(serializers.ModelSerializer):
    """Serializer for the community group"""
    status = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = "__all__"
    
    def get_status(self, instance):
        return instance.status if instance.status else 'Join'


class GroupMembershipSerializer(serializers.ModelSerializer):
    """Serializer for the community group"""
    groupid = GroupSerializer(read_only=True)
    userid = UserSerializer(read_only=True)

    class Meta:
        model = GroupMembership
        fields = "__all__"
        read_only_fields = ('id',)    
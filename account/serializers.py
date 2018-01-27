""" Account serializer"""
import messages

from django.conf import settings
from django.contrib.auth import authenticate
from django.utils import timezone
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.authtoken.models import Token

User = get_user_model()


class LoginSerializer(serializers.Serializer):
    """
       serializer for login view 
    """
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(
        min_length=4, style={'input_type': 'password'})

    default_error_messages = {
        'inactive_account': messages.INACTIVE_ACCOUNT_ERROR,
        'invalid_credentials': messages.INVALID_CREDENTIALS_ERROR
    }

    user = None

    def validate(self, attrs):
        """ check username and password """
        self.user = authenticate(username=attrs.get(User.USERNAME_FIELD),
                                 password=attrs.get('password'))
        if not self.user:
            raise serializers.ValidationError(
                self.error_messages['invalid_credentials'])
        return attrs

    def validate_username(self, value):
        """validate email id, check account exists for this email id  """
        try:
            self.user = User.objects.get(username=value)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                self.error_messages['invalid_credentials']
            )
        return value


class TokenSerializer(serializers.ModelSerializer):
    """
    user token serializers 
    """
    auth_token = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id', 'auth_token', 'first_name', 'last_name'
        )

    def get_auth_token(self, obj):
        token, _ = Token.objects.get_or_create(user=obj)
        return token.key


class RegistrationSerializer(serializers.ModelSerializer):
    """
    serializer for registering new user
    """
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password')

    def validate_email(self, email):
        """ check user name with this email id exists or not """
        try:
            User.objects.get_user_by_email(email)
        except User.DoesNotExist:
            return email
        raise serializers.ValidationError(
            messages.EMAIL_ALREADY_EXITS
        )

    def create(self, validated_data):
        """ create user """
        user = User.objects.create_user(**validated_data)
        return user


class ForgotPasswordSerializer(serializers.Serializer):
    """ user forgot email serializer fields """
    email = serializers.EmailField()
    user = None

    def validate_email(self, value):
        """ check email id exists in database or not  """
        try:
            self.user = User.objects.get_user_by_email(value)
        except User.DoesNotExist:
            raise serializers.ValidationError(messages.UNREGISTERED_EMAIL)
        return value


class UserProfileSerializer(serializers.ModelSerializer):
    """ User Profile serializer """

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email')


class UidAndTokenSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()

    default_error_messages = {
        'invalid_token': messages.INVALID_TOKEN_ERROR,
        'invalid_uid': messages.INVALID_UID_ERROR,
    }

    def validate_uid(self, value):
        try:
            uid = urlsafe_base64_decode(value)
            self.user = User.objects.get(pk=uid)
        except (User.DoesNotExist, ValueError,
                TypeError, OverflowError) as error:
            raise serializers.ValidationError(
                self.error_messages['invalid_uid'])
        return value

    def validate(self, attrs):
        attrs = super(UidAndTokenSerializer, self).validate(attrs)
        if not self.context['view'].token_generator.check_token(
                self.user, attrs['token']):
            raise serializers.ValidationError(
                self.error_messages['invalid_token'])
        return attrs


class PasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(
        style={'input_type': 'password'})


class PasswordResetConfirmSerializer(UidAndTokenSerializer, PasswordSerializer):
    pass


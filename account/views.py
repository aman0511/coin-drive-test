"""
account api
"""

from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.conf import settings

from rest_framework import generics, permissions, response, status, filters
from rest_framework.authtoken.models import Token
from utils.email import EmailMixin

from . import serializers as account_serializer
from . import models as account_model


class LoginView(generics.GenericAPIView):

    """ Api for the user login """

    serializer_class = account_serializer.LoginSerializer
    permission_classes = (
        permissions.AllowAny,
    )

    def post(self, request, *args, **kargs):
        """
        login api
        """
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            # take the user from serializer objects
            user = serializer.user
            token_serializer = account_serializer.TokenSerializer(
                instance=user)
            return response.Response(
                data=token_serializer.data,
                status=status.HTTP_200_OK,
            )


class LogoutView(generics.GenericAPIView):
    """ log out the user """
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        """ post method for the logout the user """
        Token.objects.filter(user=request.user).delete()
        return response.Response({'msg': "user logout successfully."}, status=status.HTTP_200_OK)



class ForgotPasswordView(generics.GenericAPIView, EmailMixin):
    """ user forgot password api view  """
    permission_classes = (
        permissions.AllowAny,
    )
    serializer_class = account_serializer.ForgotPasswordSerializer

    html_body_template_name = "reset_password.html"
    subject_template_name = "reset_password_subject.txt"

    def get_activation_url(self, user):
        """ get the activation url  """
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        uid = uid.decode('utf-8')
        token = default_token_generator.make_token(user)
        url = settings.ADMIN_DASHBOARD_URL['reset_password'].format(uid, token)
        print(url)
        return url

    def get_email_context(self, user):
        """ get the email context for the template """

        context = {
            'name': user.email,
            'url': self.get_activation_url(user)
        }
        return context

    def post(self, request, *args, **kwargs):
        """ send reset password mail to the end user """

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.user
            context = self.get_email_context(user)
            self.send_email(user.get_user_email(), **context)
            return response.Response({'msg': "Reset password mail has been sent on your email"})


class PasswordResetView(generics.GenericAPIView):
    """
    Use this endpoint to finish reset password process.
    """
    serializer_class = account_serializer.PasswordResetConfirmSerializer
    permission_classes = (
        permissions.AllowAny,
    )
    token_generator = default_token_generator

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={'view': self})
        if serializer.is_valid(raise_exception=True):
            serializer.user.set_password(
                serializer.validated_data['new_password'])
            serializer.user.is_active = True
            serializer.user.save()
            return response.Response({'message': "success"}, status=status.HTTP_200_OK)


class UserProfileView(generics.GenericAPIView):
    """User profile deatils """
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = account_serializer.UserProfileSerializer

    def get(self, request, *args, **kwargs):
        """ get the login user details """

        serializer = self.serializer_class(instance=request.user)
        return response.Response(serializer.data, status=status.HTTP_200_OK)


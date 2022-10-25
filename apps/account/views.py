from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated

from .serializers import (
    UserRegistartionSerializer,
    PasswordChangeSerializer,
    RestorepasswordSerializer,
    SetRestoredPasswordSerializer,
)


User = get_user_model()


class RegistrationView(APIView):
    @swagger_auto_schema(request_body=UserRegistartionSerializer)
    def post(self, request: Request):
        serializer = UserRegistartionSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                'thanks for registartion! activate your account via link in your mail',
                status=status.HTTP_201_CREATED
            )


class AccountActivationView(APIView):
    def get(self, request, activation_code):
        user = User.objects.filter(activation_code=activation_code).first()
        if not user:
            return Response(
                'page not found', 
                status=status.HTTP_404_NOT_FOUND
                )
        user.is_active = True
        user.activation_code = ''
        user.save()
        return Response(
            'account activated! you can login now',
            status=status.HTTP_200_OK
        )


class PasswordChangeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request):
        serializer = PasswordChangeSerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.set_new_password()
            return Response(
                'password changed seccesfully!',
                status=status.HTTP_200_OK
            )

class RestorePassworsView(APIView):
    def post(self, request):
        serializer = RestorepasswordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.send_code()
            return Response(
                'code was sent to your email',
                 status=status.HTTP_200_OK
            )

class SetRestoredPasswordView(APIView):
    def post(self, request: Request):
        serializer = SetRestoredPasswordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.set_new_password()
            return Response(
                'password restored successfuly',
                status=status.HTTP_200_OK
            )

class DeleteAccountView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request: Request):
        username = request.user.username
        User.objects.get(username=username).delete()
        return Response(
            'account deleted successfuly',
            status=status.HTTP_204_NO_CONTENT
        )
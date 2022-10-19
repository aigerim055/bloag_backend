from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema

from .serializers import UserRegistartionSerializer


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







# TODO: смена пароля, удаление аккаунта, восстановление пароля
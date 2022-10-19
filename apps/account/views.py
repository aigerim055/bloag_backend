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

# TODO: активация, смена пароля, удаление аккаунта, восстановление пароля
# TODO: подключить celery, redis
# TODO: исправить html

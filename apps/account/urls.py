from django.urls import path
from .views import (
    RegistrationView,
    AccountActivationView,
    PasswordChangeView,
    RestorePassworsView,
    SetRestoredPasswordView,
    DeleteAccountView,
    )

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('register/', RegistrationView.as_view(), name='registration'),
    path('activate/<str:activation_code>/', AccountActivationView.as_view(), name='activation'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('change-password/', PasswordChangeView.as_view(), name='change_pasword'),
    path('restore-password', RestorePassworsView.as_view(), name='restore_pasword'),
    path('set-restored-password', SetRestoredPasswordView.as_view(), name='set_restored_password'),
    path('delete-account', DeleteAccountView.as_view(), name='delete_account'),
]


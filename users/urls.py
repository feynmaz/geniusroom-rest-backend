from django.urls import path
from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django_rest_passwordreset.views import reset_password_request_token, reset_password_confirm, reset_password_validate_token
from .views import *

app_name = 'users'

urlpatterns = [

    path(
        route='token/',
        view=TokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),
    path(
        route='token/refresh/',
        view=TokenRefreshView.as_view(),
        name='token_refresh'
    ),
    path(
        route='register/',
        view=RegisterUserView.as_view(),
        name='register',
    ),
    path(
        route='password_reset/confirm/',
        view=reset_password_confirm,
        name='confirm_reset'
    ),
    path(
        route='password_reset/validate_token/',
        view=reset_password_validate_token,
        name='validate_reset'
    ),
    path(
        route='password_reset/',
        view=reset_password_request_token,
        name='password_reset'
    ),



]

urlpatterns = format_suffix_patterns(urlpatterns)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
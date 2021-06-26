from rest_framework import generics

from .serializers import *


class RegisterUserView(generics.CreateAPIView):
    serializer_class = UserSerializer

from rest_framework import generics, status
from rest_framework.utils.representation import serializer_repr

from apps.api.user.serializers import LoginSerializer, TokenSerializers
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data) #1:1 to user/views(POST). Taking and checking info
        serializer.is_valid(raise_exception=True)
        user = authenticate(**serializer.data)
        if user:
            token = Token.objects.filter(user=user).first()
            if not token:
                token = Token.objects.create(user=user)
            token_serializer = TokenSerializers(data={'token': token.key})
            token_serializer.is_valid()
            return Response(data=token_serializer.data, status=status.HTTP_200_OK)
        else:
            raise AuthenticationFailed('Invalid Login or Password.')

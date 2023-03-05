import jwt
from datetime import datetime, timedelta
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from authentication.serializers import LoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from authentication.backends import JWTAuthentication

class LoginView(APIView):
    serializer_class = LoginSerializer                #deserialize the incoming data i.e converts the json data to python datatype to later can be stores in database
    def post(self, request):
        serializer = self.serializer_class(data=request.data)     #initializing serializer     
        serializer.is_valid(raise_exception=True)                #validating username and password using LoginSerializer     
        user = serializer.validated_data
        print(user,"AAA")
        token = jwt.encode({
            'id':user['userId'],
            'username': user['username'],
            'exp': datetime.utcnow() + timedelta(minutes=60)       #to retrieve access token valid for 60 mins
        }, settings.SECRET_KEY, algorithm='HS256')                #secret key to sign the token value
        return Response({'token': token}, status=status.HTTP_200_OK)



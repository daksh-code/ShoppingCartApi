import jwt
from rest_framework import authentication, exceptions
from django.conf import settings
from django.contrib.auth.models import User
import json

class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        print("HELLOOOOOOOOOOOOOO")
        auth_data = authentication.get_authorization_header(request)
        print(len(auth_data),"auth_data_____________")
    
        if not auth_data:
            raise exceptions.AuthenticationFailed(
                'Your token is invalid,login')

        prefix, token = auth_data.decode('utf-8').split(' ')

        if len(token)==0:
            raise exceptions.AuthenticationFailed(
                'Your token is invalid,login')

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms="HS256")

            with open('users.json') as f:
                users = json.load(f)['users']
                user = None
                for u in users:                                          #checks whether the user is present in users.json or not 
                    if u['username'] == payload['username']:
                        user = u
                        print(user,"ASDFDDSDSDSASASASASDSEDDSDSSDDSDSDSDSDSDSDS")
                        break
                if user==None:
                    raise  exceptions.AuthenticationFailed('Your token is invalid,login')
            return (user, token)

        except jwt.DecodeError as identifier:
            raise exceptions.AuthenticationFailed(
                'Your token is invalid,login')
        except jwt.ExpiredSignatureError as identifier:
            raise exceptions.AuthenticationFailed(
                'Your token is expired,login')

        return super().authenticate(request)
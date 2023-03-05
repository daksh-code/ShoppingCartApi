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
from authentication.serializers import UserSerializer
import json

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


class RegistrationView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)    # Deserialize the request data into a UserSerializer object
        if serializer.is_valid():
            # Open the users JSON file and load its contents into a dictionary
            with open('users.json', 'r') as f:
                users = json.load(f)

            # Generate a new user ID by incrementing the last user ID in the list
            user_id = users['users'][-1]['userId'] + 1

            # Add the new user to the dictionary
            new_user = {
                'userId': user_id,
                'username': serializer.validated_data['username'],
                'password': serializer.validated_data['password'],
            }
            users['users'].append(new_user)

            # Write the updated dictionary back to the JSON file
            with open('users.json', 'w') as f:
                json.dump(users, f, indent=4)

            # Return a success response with the new user ID
            return Response({'userId': user_id}, status=status.HTTP_201_CREATED)
        else:
            # Return an error response with the validation errors
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



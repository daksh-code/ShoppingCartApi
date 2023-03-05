import json
from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):          #validating the credentials provided by the user
        
        username = data.get('username')
        password = data.get('password')

        if username and password:
            with open('users.json') as f:
                users = json.load(f)['users']
                user = None
                for u in users:                                          #checks whether the user is present in users.json or not 
                    if u['username'] == username:
                        user = u
                        break
                if user and user['password'] == password:             #checks whether password is correct or not
                    return user
                else:
                    raise serializers.ValidationError('Invalid login credentials')
        else:
            raise serializers.ValidationError('Username and password are required')



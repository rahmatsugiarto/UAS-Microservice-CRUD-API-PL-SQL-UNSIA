
import json

from authentication.jwt import create_access_token
from users import models, serializers
from users.helper import AESDecrypt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class AuthViewset(APIView):
    def post(self, request):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        usernameBody = body["username"]
        passwordBody = (body["password"])
        
        existingUser = models.Users.objects.filter(username=usernameBody).exists()
        if existingUser:
            userData = models.Users.objects.get(username=usernameBody)
            passwordDecrypt = AESDecrypt(userData.password)
            
            if passwordBody == passwordDecrypt:
                token = create_access_token(userData.id)
                item = models.Users.objects.get(id=userData.id)
                
                data = {
                    "name" : userData.name,
                    "gender" : userData.gender,
                    "username" : userData.username,
                    "password" : userData.password,
                    "token" : token,
                  }
        
                serializer = serializers.UsersSerializer(item, data=data, partial=True)
                
                if serializer.is_valid():
                     serializer.save()
                     return Response({"status": "success", "message": "Successful login", "token": token},status=status.HTTP_200_OK)
                else:
                    return Response({"status": "error", "message":"Error" }, status=status.HTTP_400_BAD_REQUEST)

            else:
                return Response({"status": "error", "message":"Password wrong" }, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"status": "error", "message":"Username does not exist" }, status=status.HTTP_400_BAD_REQUEST)
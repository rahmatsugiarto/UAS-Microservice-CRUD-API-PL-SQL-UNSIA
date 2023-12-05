from django.shortcuts import render

import json
from users.helper import AESDecrypt
from users import models
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
                return Response({"status": "success", "message": "Successful login"}, status=status.HTTP_200_OK)
            else:
                return Response({"status": "error", "message":"Password wrong" }, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "message":"Username does not exist" }, status=status.HTTP_200_OK)
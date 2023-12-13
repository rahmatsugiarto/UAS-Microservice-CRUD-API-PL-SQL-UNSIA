import json

from users.helper import AESEncrypt
from . import models
from . import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class UsersViewset(APIView):
    def get(self, request):
        id = request.GET.get("id")
        authorization_header = request.headers.get('Authorization')
        if authorization_header:
            token_parts = authorization_header.split()
            token = token_parts[0]
            
            existingToken = models.Users.objects.filter(token=token).exists()
            
            if existingToken == False:
                return Response({"status": "error","message": "invalid token."}, status=status.HTTP_401_UNAUTHORIZED)

            if id:
                existingId = models.Users.objects.filter(id=id).exists()
            
                if existingId == False:
                    return Response({"status": "error", "message": "Users does not exist"},status=status.HTTP_400_BAD_REQUEST)  

                item = models.Users.objects.get(id=id)
                serializer = serializers.UsersSerializer(item)
                return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

            items = models.Users.objects.all().order_by('id')
            serializer = serializers.UsersSerializer(items, many=True)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error","message": "invalid token."}, status=status.HTTP_401_UNAUTHORIZED)
        
        


    def post(self, request):
        authorization_header = request.headers.get('Authorization')
        
        if authorization_header:
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)

            passwordEncrypt = AESEncrypt(body['password'])
            username = body["username"]
            existingUser = models.Users.objects.filter(username=username).exists()

            data = {
                "name" : body["name"],
                "gender" : body["gender"],
                "username" : body["username"],
                "password" : passwordEncrypt,
            }
            serializer = serializers.UsersSerializer(data = data)

            if existingUser:
                return Response({"status": "error", "message": "Username already exists, please use another username"}, status=status.HTTP_400_BAD_REQUEST)
            elif serializer.is_valid():
                serializer.save()
                return Response({"status": "success","message": "Successfully created a user account", "data": serializer.data}, status=status.HTTP_201_CREATED)
            else:
                return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"status": "error","message": "invalid token."}, status=status.HTTP_401_UNAUTHORIZED)

    def patch(self, request):
        id = request.GET.get("id")
        authorization_header = request.headers.get('Authorization')
        
        if authorization_header:
            existingId = models.Users.objects.filter(id=id).exists()
            if existingId == False:
                return Response({"status": "error", "message": "Users does not exist"})  

            item = models.Users.objects.get(id=id)

            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)

            passwordEncrypt = AESEncrypt(body['password'])
            username = body["username"]
            existingUser = models.Users.objects.filter(username=username).exists()

            data = {
                "name" : body["name"],
                "gender" : body["gender"],
                "username" : body["username"],
                "password" : passwordEncrypt,
            }

            serializer = serializers.UsersSerializer(item, data=data, partial=True)


            if existingUser:
                return Response({"status": "error", "message": "Username already exists, please use another username"}, status=status.HTTP_404_NOT_FOUND)
            elif serializer.is_valid():
                serializer.save()
                return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"status": "error","message": "invalid token."}, status=status.HTTP_401_UNAUTHORIZED)
        
    def delete(self, request):
        id = request.GET.get("id")
        authorization_header = request.headers.get('Authorization')
        if authorization_header:
            existingId = models.Users.objects.filter(id=id).exists()

            if existingId:
                item = models.Users.objects.filter(id=id)
                print(item)
                item.delete()
                return Response({"status": "success", "message": "Users Deleted"})  
            else:
                return Response({"status": "error", "message": "Users does not exist"})  
        else:
            return Response({"status": "error","message": "invalid token."}, status=status.HTTP_401_UNAUTHORIZED)
        
        
        
class UsersByPassViewset(APIView):
    def post(self, request):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        
        passwordEncrypt = AESEncrypt(body['password'])
        username = body["username"]
        existingUser = models.Users.objects.filter(username=username).exists()
        
        data = {
            "name" : body["name"],
            "gender" : body["gender"],
            "username" : body["username"],
            "password" : passwordEncrypt,
        }
        serializer = serializers.UsersSerializer(data = data)
        
        if existingUser:
            return Response({"status": "error", "message": "Username already exists, please use another username"}, status=status.HTTP_400_BAD_REQUEST)
        elif serializer.is_valid():
            serializer.save()
            return Response({"status": "success","message": "Successfully created a user account", "data": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
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
        
        if id:
            existingId = models.Users.objects.filter(id=id).exists()
            if existingId == False:
                return Response({"status": "error", "message": "Users does not exist"})  
            
            item = models.Users.objects.get(id=id)
            serializer = serializers.UsersSerializer(item)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

        items = models.Users.objects.all().order_by('id')
        serializer = serializers.UsersSerializer(items, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

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
            return Response({"status": "error", "message": "Username already exists, please use another username"}, status=status.HTTP_200_OK)
        elif serializer.is_valid():
            serializer.save()
            return Response({"status": "success","message": "Successfully created a user account", "data": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        id = request.GET.get("id")
        
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
            return Response({"status": "error", "message": "Username already exists, please use another username"}, status=status.HTTP_200_OK)
        elif serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        id = request.GET.get("id")
        existingId = models.Users.objects.filter(id=id).exists()
        
        if existingId:
            item = models.Users.objects.filter(id=id)
            print(item)
            item.delete()
            return Response({"status": "success", "message": "Users Deleted"})  
        else:
            return Response({"status": "error", "message": "Users does not exist"})  
        
        
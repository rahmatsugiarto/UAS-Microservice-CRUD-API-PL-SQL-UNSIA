import json

from users.helper import AESEncrypt
from . import models
from . import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class UsersViewset(APIView):
    def get(self, request):
        # Check if there is a 'username' parameter in the request
        id = request.GET.get('id', None)
        try:
            if id:
                # Get specific user
                user = models.Users.objects.get(id=id)
                models.UserLogger.objects.create(
                    method="GET", message="Get user with id: " + str(id))
                serializer = serializers.UsersSerializer(user)
                serializer_data = serializer.data
                return Response({
                    "status": "success",
                    "data": serializer_data},
                    status=status.HTTP_200_OK)

            else:
                # Get all users
                users = models.Users.objects.all().order_by('id')
                models.UserLogger.objects.create(
                    method="GET", message="Get all users")
                serializer = serializers.UsersSerializer(users, many=True)
                serializer_data = serializer.data
                return Response({
                    "status": "success",
                    "data": serializer_data},
                    status=status.HTTP_200_OK)
                
                
        except Exception as e:
            return Response({
                "status": "error", 
                "message": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        
        
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
            return Response({
                "status": "error", 
                "message": "Username already exists, please use another username"}, 
                status=status.HTTP_400_BAD_REQUEST)
        elif serializer.is_valid():
            serializer.save()
            models.UserLogger.objects.create(
                    method="POST", message="Save user with username: " + username)
            serialized_data = serializer.data
            return Response({
                "status": "success",
                "message": "Successfully created a user account", 
                "data": serialized_data}, 
                status=status.HTTP_201_CREATED)
        else:
            return Response({
                "status": "error", 
                "data": serializer.errors}, 
                status=status.HTTP_400_BAD_REQUEST)
        # else:
        #     return Response({"status": "error","message": "invalid token."}, status=status.HTTP_401_UNAUTHORIZED)

    def patch(self, request):
        id = request.GET.get("id")
        authorization_header = request.headers.get('Authorization')
        is_login = False
        if authorization_header != None:
            is_login = models.Users.objects.filter(token=authorization_header).exists()
        
        if is_login:
            existingId = models.Users.objects.filter(id=id).exists()
            if existingId == False:
                return Response({
                    "status": "error", 
                    "message": "Users does not exist"})  

            item = models.Users.objects.get(id=id)

            itemOldName = item.name
            itemOldGender = item.gender
            itemOldUsername = item.username
            itemOldPassword = item.password

            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)

            passwordEncrypt = AESEncrypt(body['password'])
            username = body["username"]

            if item.username != username:
                existingUser = models.Users.objects.filter(username=username).exists()
            else:
                existingUser = False

            data = {
                "name" : body["name"],
                "gender" : body["gender"],
                "username" : body["username"],
                "password" : passwordEncrypt,
            }

            serializer = serializers.UsersSerializer(item, data=data, partial=True)

            if existingUser:
                return Response({
                    "status": "error", 
                    "message": "Username already exists, please use another username"}, 
                    status=status.HTTP_400_BAD_REQUEST)
            elif serializer.is_valid():
                serializer.save()

                if(itemOldName != body["name"]):
                    models.UserLogger.objects.create(
                        method="PATCH", 
                        message="Update user with id " + str(id) + ": name from " + itemOldName + " to " + body["name"])
                if(itemOldGender != body["gender"]):
                    models.UserLogger.objects.create(
                        method="PATCH", 
                        message="Update user with id " + str(id) + ": gender from " + itemOldGender + " to " + body["gender"])
                if(itemOldUsername != body["username"]):
                    models.UserLogger.objects.create(
                        method="PATCH",
                        message="Update user with id " + str(id) + ": username from " + itemOldUsername + " to " + body["username"])
                if(itemOldPassword != passwordEncrypt):
                    models.UserLogger.objects.create(
                        method="PATCH", 
                        message="Update user with id " + str(id) + ": password")
                    
                serializer_data = serializer.initial_data
                return Response({
                    "status": "success", 
                    "data": serializer_data}, 
                    status=status.HTTP_200_OK)
            else:
                return Response({
                    "status": "error", 
                    "data": serializer.errors}, 
                    status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({
                "status": "error",
                "message": "invalid token."}, 
                status=status.HTTP_401_UNAUTHORIZED)
        

    def delete(self, request):
        id = request.GET.get("id")
        authorization_header = request.headers.get('Authorization')
        is_login = False
        if authorization_header != None:
            is_login = models.Users.objects.filter(token=authorization_header).exists()
        

        if is_login:
            existingId = models.Users.objects.filter(id=id).exists()

            if existingId:
                item = models.Users.objects.filter(id=id).first()
                item.delete()
                models.UserLogger.objects.create(
                    method="DELETE", 
                    message="Delete user with id: " + str(id) + " and username: " + item.username)
                return Response({
                    "status": "success", 
                    "message": "Users deleted"})  
            else:
                return Response({
                    "status": "error", 
                    "message": "Users does not exist"})  
        else:
            return Response({
                    "status": "error",
                    "message": "invalid token."}, 
                    status=status.HTTP_401_UNAUTHORIZED)
        
        
        
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
            return Response({
                "status": "error", 
                "message": "Username already exists, please use another username"}, 
                status=status.HTTP_400_BAD_REQUEST)
        elif serializer.is_valid():
            serializer.save()
            return Response({
                "status": "success",
                "message": "Successfully created a user account", 
                "data": serializer.data}, 
                status=status.HTTP_201_CREATED)
        else:
            return Response({
                "status": "error", 
                "data": serializer.errors}, 
                status=status.HTTP_400_BAD_REQUEST)
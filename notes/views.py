import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Note, NoteLogger
from users.models import Users
from .serializers import NotesSerializer
from users.serializers import UsersSerializer

# Create your views here.
class NotesViewset(APIView):
    def get(self, request):
        is_authenticated = request.headers.get('Authorization')
        id = request.GET.get('id', None)
        try:
            if is_authenticated:
                user = Users.objects.get(token= is_authenticated)
                if id:
                    # Get specific notes
                    note = Note.objects.get(id=id)
                    NoteLogger.objects.create(
                        method="GET", message="Get note with id: " + str(id))
            
                    if note.user.id != user.id:
                        return Response({
                            "status": "failed",
                            "message": "forbidden access"}, 
                            status= status.HTTP_403_FORBIDDEN)
                    serializer = NotesSerializer(note)
                    serializer_data = serializer.data
                    return Response({
                        "status": "success",
                        "data": serializer_data},
                        status=status.HTTP_200_OK)

                else:
                    # Get all notes
                    notes = Note.objects.filter(user=user.id)
                    NoteLogger.objects.create(
                        method="GET", message="Get all notes")
                    serializer = NotesSerializer(notes, many=True)
                    serializer_data = serializer.data
                    for data in serializer_data:
                        data.pop("created_at")
                        data.pop("updated_at")
                        data.pop("user")
                    return Response({
                        "status": "success",
                        "data": serializer_data},
                        status=status.HTTP_200_OK)
                
            else:
                return Response({
                    "status": "error",
                    "message": "invalid token."}, 
                    status=status.HTTP_401_UNAUTHORIZED)
                
                
        except Exception as e:
            return Response({
                    "status": "error", 
                    "message": str(e)}, 
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        is_authenticated = request.headers.get('Authorization')
        try:
            if is_authenticated:
                user = Users.objects.get(token= is_authenticated)
                body = json.loads(request.body.decode('utf-8'))
                note = {
                    "user": user.id,
                    "title": body["title"],
                    "content": body["content"],
                }
                serializer = NotesSerializer(data = note)
                print(serializer.is_valid())

                if serializer.is_valid():
                    serializer.save()
                    NoteLogger.objects.create(
                        method="POST", message="Save note with title: " + body["title"] + " by user: " + user.id)
                    serialized_data = serializer.data
                    return Response({
                        "status": "success",
                        "message": "Successfully created a note", 
                        "data": serialized_data}, 
                        status=status.HTTP_201_CREATED)
                
                return Response({
                    "status": "error", 
                    "data": serializer.errors}, 
                    status=status.HTTP_400_BAD_REQUEST)
                
            
            else:
                return Response({
                    "status": "error",
                    "message": "invalid token."}, 
                    status=status.HTTP_401_UNAUTHORIZED)
        
        except Exception as e:
            return Response({
                "status": "error", 
                "message": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def patch(self, request):
        id = request.GET.get('id')
        authorization_header = request.headers.get('Authorization')
        is_login = False
        if authorization_header != None:
            is_login = Users.objects.filter(token=authorization_header).exists()

        try:
            if is_login:
                existingId = Note.objects.filter(id=id).exists()
                if existingId == False:
                    return Response({
                        "status": "error", 
                        "message": "Note does not exist"})  

                item = Note.objects.get(id=id)

                itemOldTitle = item.title
                itemOldContent = item.content

                body_unicode = request.body.decode('utf-8')
                body = json.loads(body_unicode)

                data = {
                    "title" : body["title"],
                    "content" : body["content"],
                }

                serializer = NotesSerializer(item, data=data, partial=True)

                if serializer.is_valid():
                    serializer.save()
                    if(itemOldTitle != body["title"]):
                        NoteLogger.objects.create(
                            method="PATCH", message="Update note title with id: " + id + " from " + itemOldTitle + " to " + body["title"])
                    if(itemOldContent != body["content"]):
                        NoteLogger.objects.create(
                            method="PATCH", message="Update note content with id: " + id + " from " + itemOldContent + " to " + body["content"])
                        
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
        except Exception as e:
            return Response({
                "status": "error", 
                "message": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def delete(self, request):
        id = request.GET.get('id')
        authorization_header = request.headers.get('Authorization')
        is_login = False
        if authorization_header != None:
            is_login = Users.objects.filter(token=authorization_header).exists()
        
        try:
            if is_login:
                existingId = Note.objects.filter(id=id).exists()

                if existingId:
                    item = Note.objects.filter(id=id)
                    item.delete()
                    NoteLogger.objects.create(
                        method="DELETE", 
                        message="Delete note with id: " + id + " and title: " + item.title + " by user: " + item.user.id)
                    return Response({
                        "status": "success", 
                        "message": "Note deleted"})
                else:
                    return Response({
                        "status": "error", 
                        "message": "Note does not exist"})   
            
            else:
                return Response({
                    "status": "error",
                    "message": "invalid token."}, 
                    status=status.HTTP_401_UNAUTHORIZED)
        
        except Exception as e:
            return Response({
                "status": "error", 
                "message": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

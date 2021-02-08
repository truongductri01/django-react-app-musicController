from django.db.models import query
from django.http.response import JsonResponse
from .serializers import RoomSerializer, CreateRoomSerializer, UpdateRoomSerializer
from .models import Room
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response


# Create your views here.
class RoomListView(generics.ListAPIView):  # create a view which allow creating new room
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

class GetRoom(APIView):
    serializer_class = RoomSerializer
    lookup_url_kwarg = 'code'  # what query to look for in the url

    def get(self, request, format=None):
        code = request.GET.get(self.lookup_url_kwarg)
        if code != None:
            # the room will be unique or not exist
            room = Room.objects.filter(code=code)
            if len(room) > 0:
                data = RoomSerializer(room[0]).data
                # check if the person sending the request a host
                data["is_host"] = self.request.session.session_key == room[0].host
                return Response(data, status=status.HTTP_200_OK)
            return Response({"Room not Found": "Invalid Room Code."}, status=status.HTTP_404_NOT_FOUND)
        return Response({"Bad Request": "code parameter not found in request"}, status=status.HTTP_404_NOT_FOUND)

class CreateRoomView(APIView):
    serializer_class = CreateRoomSerializer

    def post(self, request, format=None):
        # Check whether the user login or not
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            guest_can_pause = serializer.data.get("guest_can_pause")
            votes_to_skip = serializer.data.get("votes_to_skip")
            host = self.request.session.session_key

            # if the host already has a room, just update the room information, else create a new room
            queryset = Room.objects.filter(host=host)
            if queryset.exists():
                room = queryset[0]
                room.guest_can_pause = guest_can_pause
                room.votes_to_skip = votes_to_skip
                room.save(update_fields=["guest_can_pause", "votes_to_skip"])
            else:  # create new Room
                room = Room(host=host, guest_can_pause=guest_can_pause, votes_to_skip =votes_to_skip)
                room.save()

            self.request.session['room_code'] = room.code  # let the backend know the person at the session is in the room
            # let the user know if the request is success
            return Response(RoomSerializer(room).data, status=status.HTTP_201_CREATED)
        return Response({"Bad Request": "Invalid data..."}, status=status.HTTP_400_BAD_REQUEST)


class JoinRoom(APIView):
    lookup_url_kwarg = "code"
    # give a post request
    def post(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        
        code = request.data.get(self.lookup_url_kwarg)
        if code != None:
            room_result = Room.objects.filter(code=code)
            if len(room_result) > 0: 
                room = room_result[0]
                self.request.session['room_code'] = code  # let the backend know the person at the session is in the room
                return Response({"message": "Room Joined!"}, status=status.HTTP_200_OK)
            return Response({"Bad Request": "Invalid room code"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"Bad Request": "Invalid post data, did not find a code key"}, status=status.HTTP_400_BAD_REQUEST)

class UserInRoom(APIView):
    def get(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        
        data = {"code": self.request.session.get("room_code")}
        return JsonResponse(data, status=status.HTTP_200_OK)

class LeaveRoom(APIView):
    def post(self, request, format=None):
        if "room_code" in self.request.session:
            self.request.session.pop("room_code")  # remove the user from the room

            # delete the room if the host leave the 
            print(self.request)
            host_id = self.request.session.session_key
            room_result = Room.objects.filter(host=host_id)
            if len(room_result) > 0:
                room = room_result[0]
                room.delete()
        return Response({"Message": "Success"}, status=status.HTTP_200_OK)

class UpdateRoom(APIView):
    
    serializer_class = UpdateRoomSerializer
    def patch(self, request, format=None): 
        if not self.request.session.exists(self.request.session.session_key):
                self.request.session.create()

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            guest_can_pause = serializer.data.get("guest_can_pause")
            votes_can_skip = serializer.data.get("votes_to_skip")
            code =serializer.data.get("code")
            queryset = Room.objects.filter(code=code)
            if not queryset.exists(): 
                return Response({"msg": "Room not found."}, status=status.HTTP_404_NOT_FOUND)

            room = queryset[0]
            user_id = self.request.session.session_key
            if room.host != user_id:
                return Response({"msg": "You are not the host of this room"}, status=status.HTTP_403_FORBIDDEN)

            room.guest_can_pause = guest_can_pause
            room.votes_to_skip = votes_can_skip
            room.save(update_fields = ['guest_can_pause', 'votes_to_skip'])
            return Response(RoomSerializer(room).data, status=status.HTTP_200_OK)
        return Response({"Bad Request": "Invalid Data..."}, status=status.HTTP_400_BAD_REQUEST)
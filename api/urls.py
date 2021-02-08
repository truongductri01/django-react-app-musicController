from django.urls import path
from .views import RoomListView, CreateRoomView, GetRoom, JoinRoom, UserInRoom, LeaveRoom, UpdateRoom

urlpatterns = [
    path("create_room", CreateRoomView.as_view()),  # generate the class into the View
    path("view_rooms", RoomListView.as_view()),
    path("get_room", GetRoom.as_view()),
    path("join_room", JoinRoom.as_view()),
    path("user_in_room", UserInRoom.as_view()),
    path("leave_room", LeaveRoom.as_view()),
    path("update_room", UpdateRoom.as_view())
]

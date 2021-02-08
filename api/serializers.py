from rest_framework import serializers
from .models import Room

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room 
        fields = ('id', 'code', 'host', 'guest_can_pause', 'votes_to_skip', 'created_at')

class CreateRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ("guest_can_pause", "votes_to_skip")  # what to send as a POST Request
        
class UpdateRoomSerializer(serializers.ModelSerializer):
    code = serializers.CharField(validators=[])  # not referring to the code in models.py
    class Meta:
        model = Room
        fields = ("guest_can_pause", "votes_to_skip", "code")  # "code" will refered to code on line 15, not from the models.py
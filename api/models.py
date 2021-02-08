from django.db import models
import string
import random

def generate_unique_code():  # generate random unique code
    length = 6
    code = ""
    while True:
        # generate randome code for the room
        code = "".join(random.choices(string.ascii_uppercase, k=length))
        # check the code is unique
        if Room.objects.filter(code=code).count() == 0:
            break
    return code


# Create your models here.
class Room(models.Model):
    # Describe the fields
    code = models.CharField(max_length=8, default=generate_unique_code, unique=True)
    host = models.CharField(max_length=50, unique=True)
    guest_can_pause = models.BooleanField(null=False, default=False)
    votes_to_skip = models.IntegerField(null=False, default=1)
    created_at = models.DateTimeField(auto_now_add=True)  # automatically add the time when the object is created
    current_song = models.CharField(max_length=50, null=True)

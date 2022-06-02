from django.db import models

# Create your models here.

class Room(models.Model):
    name = models.TextField(max_length=255, unique=True)
    capacity = models.IntegerField()
    projector = models.BooleanField()

class RoomBooking(models.Model):
    room_id = models.ForeignKey(Room, on_delete=models.CASCADE)
    date = models.DateField()
    comment = models.TextField(null=True)


class Meta:
   unique_together = ('room_id', 'date',)
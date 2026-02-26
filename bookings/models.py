from django.db import models
from accounts.models import User
from trains.models import Train

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    train = models.ForeignKey(Train, on_delete=models.CASCADE)
    seats_booked = models.IntegerField()
    booking_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return f"{self.user.email} - {self.train.train_number}"
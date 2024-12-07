from django.db import models
from django.contrib.auth.models import User
from datetime import time


class User_details(models.Model):
    objects = models.Manager()
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    # first_name = models.CharField(max_length=50,blank=False)
    # last_name = models.CharField(max_length=50,blank=False)
    contact_no = models.BigIntegerField()


    def __str__(self):
        return str(self.user_id)

class Movies(models.Model):
    objects = models.Manager()
    movie = models.CharField(max_length=50, blank=False)
    type = models.CharField(max_length=50, blank=False)
    duration = models.TimeField()
    image = models.FileField(upload_to='image',blank=False)
    rating = models.DecimalField(max_digits=5,decimal_places=2,blank=False)


    def __str__(self):
        return str(self.movie)

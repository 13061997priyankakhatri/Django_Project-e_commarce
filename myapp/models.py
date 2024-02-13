from django.db import models

# Create your models here.

class User(models.Model):
    email = models.EmailField()
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    mobile = models.PositiveBigIntegerField()
    password = models.CharField(max_length=10)


    def __str__(self):
        return self.firstname
    
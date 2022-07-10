from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField(null=False)
    phone = PhoneNumberField(null=False, blank=False, unique=True)

    def __str__(self):
        return self.name


class Poll(models.Model):
    question = models.TextField()
    user = models.ForeignKey(Profile,on_delete=models.SET_NULL,null=True,blank=True)
    option_1 = models.CharField(max_length=30)
    option_2 = models.CharField(max_length=30)
    option_3 = models.CharField(max_length=30)
    option_4 = models.CharField(max_length=30)
    option_1_votes = models.IntegerField(default=0)
    option_2_votes = models.IntegerField(default=0)
    option_3_votes = models.IntegerField(default=0)
    option_4_votes = models.IntegerField(default=0)

    def __str__(self):
        return self.question
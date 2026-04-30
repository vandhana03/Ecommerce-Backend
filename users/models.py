from django.db import models

# from django.contrib.auth.models import AbstractUser
# Create your models here.

class Users(models.Model):
    class Role(models.TextChoices):
        ADMIN="ADMIN"
        USER="USER"
    
    username=models.TextField(max_length=50,default='default user')
    password=models.TextField(max_length=30,default=12345)
    email=models.TextField(max_length=80,default='abc@gmail.com')
    role=models.CharField(max_length=10,choices=Role,default=Role.USER)
    address=models.TextField(blank=True,null=True)
    

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


class Product(models.Model):
    category_choices=(
        ('electronics','Electronics'),
        ('fashion','Fashion'),
        ('books','Books'),
        ('home','Home')
    )
    name=models.CharField(max_length=255)
    description=models.TextField()

    price=models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    category=models.CharField(
        max_length=100,
        choices=category_choices
    )
    stock_quantity=models.IntegerField(default=0)
    created_at=models.DateTimeField(auto_now_add=True)

    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
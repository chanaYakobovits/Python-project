from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    phone = models.CharField(max_length=10, blank=True)
    status = models.IntegerField(choices={1: "buyer", 2: "seller", 3: "Mediate"}, default=1)
    commission = models.FloatField(default=0)
    # FinalProfit = models.FloatField(default=0)

    def __str__(self):
        return f"{self.username}"

class Apartment(models.Model):
    city = models.CharField(max_length=30)
    street = models.CharField(max_length=30)
    floor = models.IntegerField()
    rooms = models.IntegerField()
    price = models.FloatField()
    description = models.CharField(max_length=120)
    Status = models.BooleanField(default=False)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Apartment_seller', db_column = 'Apartment_seller')

    def __str__(self):
        return f"({self.id}: {self.price}:{self.Status})"

class Image(models.Model):
    apartmentID = models.ForeignKey(Apartment,  related_name='images',on_delete=models.CASCADE)
    url = models.ImageField(upload_to='images/', blank=True, null=True)


    def __str__(self):
        return f"({self.id})"

class Request(models.Model):
    apartmentID = models.ForeignKey(Apartment,related_name='request', on_delete=models.CASCADE )
    content = models.CharField(max_length=120,null=True)
    sendUser = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return f"({self.sendUser} {self.content})"

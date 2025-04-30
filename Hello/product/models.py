from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    Name= models.CharField(max_length=100)
    DOB= models.DateField(blank=True, null=True)
    Education= models.CharField(max_length=250)

    def __str__(self):
        return self.Name



class Book(models.Model):
    Title= models.CharField(max_length=25)
    Author= models.ForeignKey(Author, on_delete=models.CASCADE)
    Descriptions= models.TextField()
    Genere= models.CharField(max_length=15)
    Price =models.DecimalField(max_digits=6 , decimal_places=2)
    Cover_Page= models.ImageField(upload_to='image/')

    def __str__(self):
        return self.Title



class Order(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    Book= models.ForeignKey(Book, on_delete=models.CASCADE)
    order_at= models.DateField(auto_now=True)

    def __str__(self):
        return f"orderd by {self.user.username}"
    

class User_registration(models.Model):

    user=models.OneToOneField(User, on_delete=models.CASCADE)

    email= models.EmailField()

    def __str__(self):
        return self.user.username





class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/', default='profile_pics/default.jpg')

    def __str__(self):
        return f"{self.user.username}'s Profile"

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
    PAYMENT_METHODS = [
        ('cash', 'Cash on Delivery'),
        ('khalti', 'Khalti'),
    ]
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHODS, default='cash')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
  
    shipping_name = models.CharField(max_length=100, default='Anonymous')
    shipping_address = models.TextField(default='Not provided')

    order_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.book.title} x {self.quantity}"

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
    
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Cart"

    def total_price(self):
        return sum(item.total_price() for item in self.cart_items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='cart_items', on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.book.Title} in {self.cart.user.username}'s cart"

    def total_price(self):
        return self.book.Price * self.quantity




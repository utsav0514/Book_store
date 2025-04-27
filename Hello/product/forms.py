from django import forms
from django.contrib.auth.models import User
from .models import Author, Book,  Order,User_registration

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['Name', 'DOB', 'Education']


class BookForm(forms.ModelForm):
    class Meta:
        model = Book 
        fields = ['Title', 'Author', 'Descriptions', 'Genere', 'Price', 'Cover_Page']



class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [] 

class User_RegistrationForm(forms.ModelForm):
    class Meta:
        model= User_registration
        fields= ['username','email']
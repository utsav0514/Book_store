from django import forms
from django.contrib.auth.models import User
from .models import Author, Book,  Order,User_registration,CartItem,Cart,Profile

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
        fields = ['shipping_name', 'shipping_address', 'payment_method']
        widgets = {
            'shipping_address': forms.Textarea(attrs={'rows': 3}),
            'payment_method': forms.RadioSelect(),  # optional for radio buttons
        }

class User_RegistrationForm(forms.ModelForm):
    class Meta:
        model= User_registration
        fields= ['email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture']

class CartForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = ['user'] 

class CartItemForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ['cart', 'book', 'quantity']
        widgets = {
            'cart': forms.HiddenInput(),  
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
       
        self.fields['quantity'].widget.attrs.update({'min': 1})  

class CheckoutForm(forms.Form):
    shipping_name = forms.CharField(max_length=100, required=True)
    shipping_address = forms.CharField(widget=forms.Textarea, required=True)
    payment_method = forms.ChoiceField(choices=Order.PAYMENT_METHODS, required=True)
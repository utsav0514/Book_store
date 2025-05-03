from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,authenticate, logout

from .forms import AuthorForm, BookForm,OrderForm,ProfileUpdateForm,Profile,CheckoutForm
from .models import *  
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import json
import requests
from django.http import JsonResponse

def home(request):
    return render(request, 'home.html' )

@login_required

def create_book(request):

    if request.method== 'POST':
        form=BookForm(request.POST , request.FILES)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form= BookForm()
    
    return render(request, 'create_book.html', {'form':form})

@login_required
def book_list(request):
    book = Book.objects.all()
    return render(request,'book_list.html', {'book': book})

@login_required
def update_book(request, pk):
   
    book = get_object_or_404(Book, pk=pk)

    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_list')  
    else:
        form = BookForm(instance=book)
    
    return render(request, 'update_book.html', {'form': form})
@login_required
def delete_book(request, pk):
    book= get_object_or_404(Book, pk=pk)
    if request.method=='POST':
        book.delete()
        return redirect('book_list')
    
    return render(request, 'delete_book.html', {'book':book})

@login_required
def create_author(request):
    if request.method =='POST':
        form=AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('author_list')
        
    else:
        form=AuthorForm()
    
    return render(request, 'create_author.html', {'form':form})
@login_required
def author_list(request):
    authors= Author.objects.all()
    return render(request, 'author_list.html', {'authors':authors} )

@login_required
def delete_author(request, pk):
    authors= get_object_or_404(Author,pk=pk)
    if request.method== 'POST':
        authors.delete()
        return redirect('author_list')
    
    return render(request, 'delete_author.html', {'authors':authors} )


def registration(request):
    if request.method== 'POST':
        username= request.POST['username']
        password =request.POST['password']
        email= request.POST['email']
    
        if User.objects.filter(username=username).exists():
               messages.error(request,"User already exist")
               return redirect('registration')
        
        user= User.objects.create_user(username=username, email=email, password=password)
        user.save()
        login(request, user)
        messages.success(request,"Registration sucessfull")
        return redirect('book_list')
    return render(request,'register.html')

def login_view(request):
    if request.method == 'POST':
        username= request.POST['username']
        password=request.POST['password']

        user= authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Logged in sucessful")
            return redirect('book_list')
        
        else:
            messages.error(request, "Invalid username or password")
    
    return render(request, 'login.html')

    
def logout_view(request):
    logout(request)  
    messages.success(request, "Logged out sucessfully") 
    return redirect('home')
          


@login_required
def buy_book(request, pk):
    book = get_object_or_404(Book, pk=pk)  

    if request.method == 'POST':
        form = OrderForm(request.POST)

        if form.is_valid():
            order = form.save(commit=False) 
            order.user = request.user  
            order.Book = book 
            order.save() 
            
            return redirect('order_success') 

    else:
        form = OrderForm()  

    return render(request, 'buy_book.html', {'form': form, 'book': book})

@login_required
def order_success(request):

    return render(request, 'order_success.html')


@login_required
def profile_view(request):

    return render(request, 'profile.html', {'user': request.user})


@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.cart_items.all()

    items = []
    total = 0
    for item in cart_items:
        item_total = item.book.Price * item.quantity

        items.append({
            'id': item.id,
            'book': item.book,
            'quantity': item.quantity,
            'price': item.book.Price,
            'item_total': item_total
        })
        total += item_total

    return render(request, 'view_cart.html', {
        'cart_items': items,
        'total': total
    })

@login_required
def add_to_cart(request, pk):
    book = get_object_or_404(Book, pk=pk)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, book=book)

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return render(request, 'add_to_cart.html', {'book': book})

@login_required
def update_cart_item(request, pk):
    item = get_object_or_404(CartItem, pk=pk, cart__user=request.user)
    if request.method == 'POST':
        new_quantity = int(request.POST.get('quantity', 1))
        if new_quantity > 0:
            item.quantity = new_quantity
            item.save()
        else:
            item.delete()
    return redirect('view_cart')


@login_required
def remove_from_cart(request, pk):
    item = get_object_or_404(CartItem, pk=pk, cart__user=request.user)
    item.delete()
    return redirect('view_cart')


def update_profile(request):

    profile, created = Profile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=profile)
    
    return render(request, 'update_profile.html', {'form': form})


@login_required
def proceed_to_checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)

    if not cart_items.exists():
        return redirect('view_cart')

    total_price = sum(item.book.Price * item.quantity for item in cart_items)

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = Order.objects.create(
                user=request.user,
                total_price=total_price,
                payment_method=form.cleaned_data['payment_method'],
                shipping_name=form.cleaned_data['shipping_name'],
                shipping_address=form.cleaned_data['shipping_address']
            )

            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    book=item.book,
                    quantity=item.quantity,
                    price=item.book.Price
                )


            cart_items.delete()

            return redirect('order_summary', order_id=order.id)
    else:
        form = CheckoutForm()

    return render(request, 'checkout.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'form': form
    })

@login_required
def order_summary(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order_items = order.orderitem_set.all()

    return render(request, 'order_summary.html', {
        'order': order,
        'order_items': order_items
    })
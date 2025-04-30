from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,authenticate, logout

from .forms import AuthorForm, BookForm,OrderForm
from .models import *  
from django.contrib.auth.models import User
from django.contrib import messages



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



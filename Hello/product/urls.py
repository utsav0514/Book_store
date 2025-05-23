from django.urls import path
from . import views

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create_book/', views.create_book, name="create_book"),
    path('book_list/', views.book_list, name='book_list'),
    path('update_book/<int:pk>/', views.update_book, name='update_book'),
    path('delete_book/<int:pk>/', views.delete_book, name='delete_book'),
    path('create_author/', views.create_author, name='create_author'),
    path('author_list/', views.author_list, name='author_list'),
    path('delete_author/<int:pk>/', views.delete_author, name='delete_author'),
    path('register/', views.registration, name="registration"),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('buy/<int:pk>', views.buy_book, name='buy_book'),
    path('order_success/', views.order_success, name='order_success'),
    path('profile/', views.profile_view, name='profile'),
    path('view_cart/', views.view_cart, name='view_cart'),  
    path('add_to_cart/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('update-cart-item/<int:pk>/', views.update_cart_item, name='update_cart_item'),

    path('remove_from_cart/<int:pk>/', views.remove_from_cart, name='remove_from_cart'),
    path('update_profile', views.update_profile, name='update-profile'),

    path('checkout/', views.proceed_to_checkout, name='checkout'),
    path('order-summary/<int:order_id>/', views.order_summary, name='order_summary'),


]
    



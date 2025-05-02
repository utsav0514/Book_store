from django.contrib import admin

from . models import Author, Book,  Order,Profile,Cart,CartItem

admin.site.register(Author)
admin.site.register(Book)

admin.site.register(Order)
admin.site.register(Profile)

admin.site.register(Cart)

admin.site.register(CartItem)
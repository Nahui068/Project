from django.contrib import admin
from .models import Book,User_info,Borrow_list,Image

# Register your models here.
admin.site.register(Book)
admin.site.register(User_info)
admin.site.register(Borrow_list)
admin.site.register(Image)
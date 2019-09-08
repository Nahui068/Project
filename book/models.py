from django.db import models
#python manage.py makemigrations
#python manage.py migrate


class Book(models.Model):
	book_id = models.CharField(max_length=20,primary_key=True)
	book_name = models.CharField(max_length=50)
	publisher = models.CharField(max_length=20)
	author =  models.CharField(max_length=15)
	year = models.IntegerField()

class User_info(models.Model):
	user_id = models.CharField(max_length=9,primary_key=True)
	user_pw = models.CharField(max_length=20,null=False,default='1234')
	user_name = models.CharField(max_length=10)
	major = models.CharField(max_length=15)
	borrow_num = models.IntegerField(default=0)
	overdue = models.DateTimeField() #언제까지 못빌리는 지

class Borrow_list(models.Model):
	book = models.ForeignKey(Book,on_delete=models.CASCADE,)
	user = models.ForeignKey(User_info,on_delete=models.CASCADE,)
	borrow_date = models.DateTimeField()
	return_date = models.DateTimeField()

class Image(models.Model):
	user = models.ForeignKey(User_info, on_delete=models.CASCADE,)
	image_path = models.CharField(max_length=50)



from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate
from django.utils import timezone
import datetime
import time 
from book import barcode
from book import face_reconize
from .models import Image, User_info, Book, Borrow_list
def index(request):
	return render(request, 'book/index.html')

def register(request): #예외 등록된 이미지가 이미 있는 경우에도 메세지 출력(html로 작동)
	if request.method =="POST":
		user_id = request.POST.get('user_id')
		user_pw = request.POST.get('user_pw')
		user_infos = User_info.objects.filter(user_id = user_id)
		if user_infos :
			for info in user_infos:
				if info.user_pw == user_pw:
					try :
						image = Image.objects.get(user = user_id)
						type = 'Yes user image'
						context_back={'type': type}
						return render(request,'book/back.html',context_back)
					except:
						image = None
					context= {'image' : image, 'User_info' :user_infos}
					return render(request,'book/register.html',context)
				else :
					return render(request,'book/login.html')
		else :
			if(user_id):
				type = 'register error'
				context_back={'type': type}
				return render(request,'book/back.html',context_back)		
			else :
				return render(request,'book/login.html')
	else : 
		return render(request,'book/login.html')


def face_register(request): #얼굴인식이 안될 경우 이 때 메세지(3회 카운트를 어떻게 할지 고민...)
	user_id = request.POST.get('user')
	users = User_info.objects.get(pk=user_id)
	start_time=time.time()
	image_=face_reconize.face_register(user_id)
	print('등록 : ',time.time()-start_time)
	if image_== 'timeout':
		type = 'time_out error'
		context_back={'type': type}
		return render(request,'book/back.html',context_back)
	elif image_ != None: 
		try :
			image = Image.objects.get(user = users, image_path = image_)
			image.save()
		except :
			image = Image(user= users ,image_path=image_)
			image.save()
	else : image = None
	user_infos = User_info.objects.filter(user_id = user_id)
	context= {'image' : image, 'User_info' :user_infos}
	return render(request,'book/register.html',context)

def borrow(request):# 대출가능한 유저인지 확인(overdue, borrow_num)=>back.html로 에러 메세지
	if request.method == "POST":
		play_borrow = request.POST.get('borrow')
		if play_borrow ==None:
			return render(request,'book/borrow.html') 
		today = timezone.now()
		start_time=time.time()
		image_borrow = face_reconize.face_regonize()
		print('인식 : ',time.time()-start_time)
		if image_borrow== 'timeout':
			type = 'time_out error'
			context_back={'type': type}
			return render(request,'book/back.html',context_back)
		image_borrow_info = Image.objects.filter(image_path = image_borrow)
		if image_borrow_info :
			image_info = Image.objects.get(image_path = image_borrow)
			user_info = User_info.objects.get(pk = image_info.user_id)
			if user_info.overdue<=today and user_info.borrow_num<=3:
				for borrow_info in image_borrow_info:
						context= {'image' : borrow_info}
						return render(request,'book/borrow.html',context)
			else :
				type = 'borrow_num error'
				context_back={'type': type}
				return render(request,'book/back.html',context_back)
		else :
			return render(request,'book/borrow.html')
	else :
		return render(request,'book/borrow.html')

def barcode_borrow(request):
	today = timezone.now()
	re_day = today+datetime.timedelta(days=7)
	user_borrow = request.POST.get('user')
	user_id = request.POST.get('barcode_user')
	if user_id != None :
		print(user_id)
		borrow_user_info = User_info.objects.get(pk=user_id)
		start_time=time.time()
		barcode_data=barcode.barcode()
		print('바코드인식 : ',time.time()-start_time)
		if barcode_data== 'timeout':
			type = 'time_out error'
			context_back={'type': type}
			return render(request,'book/back.html',context_back)
		try : 
			book_yn = Book.objects.get(pk = barcode_data)
		except: 
			type = 'book_yn error'
			context_back={'type': type, 'user_id': user_id}
			return render(request,'book/back.html',context_back)
		try : 
			borrow_yn = Borrow_list.objects.get(book_id = barcode_data)
		except :
			borrow_yn=None
		if borrow_yn == None :	
			try : 
				borrow_book_info = Book.objects.get(pk = barcode_data)
				if borrow_book_info == None :
					context= {'Borrow' :borrow_info, 'user_id' : user_id}
					return render(request,'book/borrow_barcode.html',context)
				borrow_info = Borrow.objects.get(user= borrow_user_info ,book= borrow_book_info, borrow_date = today.strftime("%Y-%m-%d"), return_date= re_day.strftime("%Y-%m-%d"))
				borrow_info.save()
			except :
				borrow_info = Borrow_list(user= borrow_user_info,book= borrow_book_info,borrow_date = today.strftime("%Y-%m-%d"), return_date=re_day.strftime("%Y-%m-%d"))
				borrow_info.save()
			borrow_user_info.borrow_num+=1
			borrow_user_info.save()
			context= {'Borrow' :borrow_info, 'user_id' : user_id}
			return render(request,'book/borrow_barcode.html',context)
		else :
			type = 'borrow_yn error'
			context_back={'type': type}
			return render(request,'book/back.html',context_back)
						
	else : borrow_info = None
	context= {'Borrow' :borrow_info, 'user_id' : user_borrow}
	return render(request,'book/borrow_barcode.html',context)


def _return(request):
	if request.method == "POST":
		play_return = request.POST.get('barcode')
		if play_return!=None:
			today = timezone.now()
			barcode_return=barcode.barcode()

			if barcode_return == 'timeout':
				type = 'time_out error'
				context_back={'type': type}
				return render(request,'book/back.html',context_back)
			try : 
				book_yn = Book.objects.get(pk = barcode_return)
			except: 
				type = 'book_yn error'
				context_back={'type': type}
				return render(request,'book/back.html',context_back)
			return_book_info = Borrow_list.objects.filter(book_id = barcode_return)
			if return_book_info:
				return_info = Borrow_list.objects.get(book_id = barcode_return)
				user_info = User_info.objects.get(pk=return_info.user_id)
				overdue = today-return_info.return_date
				days = overdue.days
				if overdue.days > 0:
					user_info.overdue = today+overdue
				else:
					user_info.overdue = today 
				user_info.save()
				if user_info.borrow_num > 0:
					user_info.borrow_num-=1
					user_info.save()
				return_book_info.delete()
				context= {'Returns' : user_info}
				return render(request,'book/return.html',context)
			else:
				type = 'Yes Returns'
				context_back={'type': type}
				return render(request,'book/back.html',context_back)
		else :
			return render(request,'book/return.html')
	else :
		return render(request,'book/return.html')
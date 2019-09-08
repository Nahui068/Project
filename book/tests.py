from django.test import TestCase
from . import views
# Create your tests here.
from django.shortcuts import render,redirect
from django.http import HttpResponse,StreamingHttpResponse,HttpResponseRedirect
from django.urls import reverse
import cv2
import time
from django.views.decorators import gzip


class VideoCamera(object):
	def __init__(self):
		self.video = cv2.VideoCapture(0)
	def __del__(self):
		self.video.release()

	def get_frame(self):
		ret,image = self.video.read()
		ret,jpeg = cv2.imencode('.jpg',image)
		return jpeg.tobytes()

def gen(camera):
	while True:
		frame = camera.get_frame()
		yield(frame)
		time.sleep(1)

@gzip.gzip_page
def index(request):
		#return StreamingHttpResponse(gen(VideoCamera()),content_type="image/jpeg") 
#try:
		return HttpResponse(gen(VideoCamera()),content_type="multipart/x-mixed-replace;boundary=frame")
#	except HttpResponseServerError as e:
#		print("aborted")

from django.views.decorators.http import condition

@condition(etag_func=None)
def stream(request):
	
    #resp = HttpResponse(stream_response_generator())
    return render(request,'book/test.html')

import pyzbar.pyzbar as pyzbar
import cv2
def barcode(request):
	cap = cv2.VideoCapture(cv2.CAP_DSHOW)
	ret,img= cap.read()
	i = 0
	barcode_data= None
	#try:
	while(True):
		ret, img = cap.read()
		if not ret:
			continue
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		decoded = pyzbar.decode(gray)
		cv2.imshow('img',img)
		print(decoded)
		if ((cv2.waitKey(1) & 0xFF == ord('q')) or decoded!=[]) :
			for d in decoded:
				barcode_data = d.data.decode("utf-8")
				print(barcode_data)
				cap.release()
				cv2.destroyAllWindows()
				return render(request,'book/test.html',{'barcode':barcode_data})
	return render(request,'book/test.html',{'barcode':barcode_data})
	#except:
		#return render(request,'book/test.html')	
	#<img width="400" height="400" src="http://192.168.35.73:4747/videofeed">
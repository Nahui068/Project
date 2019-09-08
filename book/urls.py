from django.urls import path,include
from . import views
from . import tests
from django.contrib.auth import views as auth_views

urlpatterns=[path('', views.index),
			path('register',views.register),
			path('face_register',views.face_register),
			path('borrow', views.borrow),
			path('barcode_borrow',views.barcode_borrow),
			path('return', views._return),
			#test
			path('test', tests.stream),
			path('barcode', tests.barcode)
			]

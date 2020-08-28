from django.contrib import admin
from django.urls import path,include
from .views import index,logged,payment_done,payment_canceled,process_subscription,download_file
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('',index,name='index'),
    path('logged/',logged,name='logged'),
    path('logged/download/', download_file),
    path('payment_done/',payment_done,name='payment_done'),
    path('payment_canceled/', payment_canceled, name='payment_canceled'),



]

from django.conf.urls import url
from django.urls import path
from . import views

app_name='payment'

urlpatterns = [
    path(r'process/', views.payment_process, name='process'),
    path(r'done/', views.payment_done, name='done'),
    path(r'canceled/', views.payment_canceled, name='canceled'),

]
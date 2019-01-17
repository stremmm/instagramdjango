from django.urls import path, re_path, include
from . import views

from accounts.models import *
from accounts.views import *

app_name = 'accounts'

urlpatterns = [
    path(r'subscription/', views.subscription_view, name='subscription_view'),
    path(r'signup/', views.signUp_view, name='signup'),
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.activate, name='activate'),
]


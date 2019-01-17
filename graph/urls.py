from django.urls import path
from django.conf.urls import url
from . import views
from .views import history_data_view, heart_feed_view

from graph.views import *

app_name = 'graph'

urlpatterns = [
    url(r'^$', views.graph_detail, name='graph_detail'),
    url(r'api/historydata/', history_data_view.as_view(), name='history_data'),
    url(r'api/feeddata/', heart_feed_view.as_view(), name='feed_data'),
    path(r'editaccount/', views.edit_account_view, name='edit_account_view'),
    path(r'editpreferences/', views.edit_preferences_view, name='edit_preferences_view'),
    path(r'remove/<x>', views.deletehistory_view, name='deletehistory_view'),
]
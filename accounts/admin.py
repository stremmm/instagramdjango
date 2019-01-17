from django.contrib import admin

from .models import Subscription


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('accountuser', 'ordernumber', 'substart', 'subend', 'active', 'isrunning')


    

admin.site.register(Subscription, SubscriptionAdmin)

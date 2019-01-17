from django.shortcuts import render, redirect, get_object_or_404
from graph.instaapi import instaStats, recentStats, timeCompare

from django.contrib.auth.models import User

import datetime
import time

from graph.forms import *
from graph.models import *

import dateutil.parser
from django.utils import formats

#Django Rest Framework
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers


# Create your views here.
def graph_detail(request):
    user = request.user
    dataGeneral = None
    dataRecent = None
    dataRecentTime = None
    dataRecentTime2 = None
    uploadTimeDifference = None
    uploadTimeDifferenceFormat = None
    info = None
    form = None

    try: 
        info = UserInfo.objects.get(accountuser = user)

        #Account Info
        instastats = instaStats()
        statinfo = instastats.returnStats(info.clientid, info.accesstoken)
        dataGeneral = statinfo['data']
        #available data: id, username, profile_picture, full_name, bio, is_business, counts : media, follows, followed_by

        #Last Upload Info
        instarecentmedia = recentStats()
        statrecent = instarecentmedia.recentMediaInfo(info.accesstoken, 1)
        dataRecent = statrecent['data']
        dataRecent = dataRecent[0]

        checktime = int(dataRecent['created_time'])    

        compareTime = timeCompare()
        dataRecentTime = timeCompare.epochtime(checktime)


        dataRecentTime2 = dateutil.parser.parse(dataRecentTime)

        #print(dataRecentTime2)
        #available data: id, user, full_name, profile_picture, username, images: (choose from thumbnail, low_resolution, standard_resolution): width, height, url, created_time, caption: id, text, and more

        #comparing current time to last upload time
        uploadTimeDifference = timeCompare.uploadTime(checktime)


        if uploadTimeDifference > 86400:
            days = uploadTimeDifference // 86400
            hours = uploadTimeDifference // 3600 % 24
            minutes = uploadTimeDifference // 60 % 60
            seconds = uploadTimeDifference % 60
            uploadTimeDifferenceFormat = "{}{}{}{}{}{}{}{}".format(days, " Days, ", hours, " Hours ", minutes, " Minutes, ", seconds, " Seconds")
        elif uploadTimeDifference > 3600 and uploadTimeDifference < 86400:
            hours = uploadTimeDifference // 3600 % 24
            minutes = uploadTimeDifference // 60 % 60
            seconds = uploadTimeDifference % 60
            uploadTimeDifferenceFormat = "{}{}{}{}{}{}".format(hours, " Hours ", minutes, " Minutes, ", seconds, " Seconds")
        elif uploadTimeDifference > 60 and uploadTimeDifference < 3600:
            minutes = uploadTimeDifference // 60 % 60
            seconds = uploadTimeDifference % 60
            uploadTimeDifferenceFormat = "{}{}{}{}".format(minutes, " Minutes, ", seconds, " Seconds")
        elif uploadTimeDifference < 60:
            seconds = uploadTimeDifference % 60
            uploadTimeDifferenceFormat = "{}{}".format( seconds, " Seconds")



        #uploadTimeDifferenceFormat = str(days, " Days,", hours, " Hours,", minutes, " Minutes,", seconds, " Seconds")
        #print(uploadTimeDifferenceFormat)
        #print(days, " Days,", hours  )
        #delete history
        form = deletehistory_form(request.POST or None)
    
    except:
        print('error')


    context = {
        'info': info,
        'dataGeneral': dataGeneral,
        'dataRecent': dataRecent,
        'dataRecentTime': dataRecentTime,
        'dataRecentTime2': dataRecentTime2,
        'uploadTimeDifference': uploadTimeDifference,
        'uploadTimeDifferenceFormat': uploadTimeDifferenceFormat,
        'form': form,
    }

    return render(request, 'graph/detail.html', context)

def deletehistory_view(request, x):
    #address = get_object_or_404(LikeHistory, accountuser = x)      
    if request.method == 'POST':
        try:
            deletehistory = LikeHistory.objects.filter(accountuser__username = x)
            deletehistory.delete()
        except:
            print('delete history not working')
        return redirect('/')



def edit_account_view(request):
    user = request.user
    info = None

    try: 
        info = UserInfo.objects.get(accountuser = user)
    except: 
        print('error')
   


    form = userinfo_Form(request.POST or None)
    if form.is_valid():
        try:
            #if already in db 
            update = UserInfo.objects.get(accountuser = user)
            update.instauser = form.cleaned_data['instauser']
            update.instapass = form.cleaned_data['instapass']
            update.clientid = form.cleaned_data['clientid']
            update.accesstoken = form.cleaned_data['accesstoken']
            update.startdate = datetime.datetime.today()
            update.save()
            return redirect('/graph/editaccount')
            
            

        except:
            instauser = form.cleaned_data['instauser']
            instapass = form.cleaned_data['instapass']
            clientid = form.cleaned_data['clientid']
            accesstoken = form.cleaned_data['accesstoken']
            startdate = datetime.datetime.today()

            
            insert = UserInfo(accountuser = user, instauser = instauser, instapass = instapass, clientid = clientid, accesstoken = accesstoken, startdate = startdate)
            insert.save()
            
            return redirect('/graph/editaccount')

    context = {
        'form': form,
        'user': user,
        'info': info,
    }
    return render(request, 'graph/editaccount.html', context)

def edit_preferences_view(request):
    user = request.user
    info = None

    getcategories = InstaCategories.objects.all()

    try: 
        info = LikingPreferences.objects.get(accountuser = user)
    except:
        print('error')

    form = likingpreferences_Form(request.POST or None)
    if form.is_valid():
        try:
            #if already set
            update = LikingPreferences.objects.get(accountuser = user)
            update.likesperhour = form.cleaned_data['likesperhour']
            update.consecutivehours = form.cleaned_data['consecutivehours']
            update.likesperday = form.cleaned_data['likesperday']
            update.minposts = form.cleaned_data['minposts']
            update.maxfollowers = form.cleaned_data['maxfollowers']
            update.minfollowers = form.cleaned_data['minfollowers']
            update.enforceclarifai = form.cleaned_data['enforceclarifai']
            update.enforcebanned = form.cleaned_data['enforcebanned']
            update.subscribedcategories = form.cleaned_data['subscribedcategories']
            update.save()
            return redirect('/graph/editpreferences')
            
            

        except:
            likesperhour = form.cleaned_data['likesperhour']
            consecutivehours = form.cleaned_data['consecutivehours']
            likesperday = form.cleaned_data['likesperday']
            minposts = form.cleaned_data['minposts']
            maxfollowers = form.cleaned_data['maxfollowers']
            minfollowers = form.cleaned_data['minfollowers']
            enforceclarifai = form.cleaned_data['enforceclarifai']
            enforcebanned = form.cleaned_data['enforcebanned']
            subscribedcategories = form.cleaned_data['subscribedcategories']

            insert = LikingPreferences(accountuser = user, likesperhour = likesperhour, consecutivehours = consecutivehours, likesperday = likesperday, minposts = minposts, maxfollowers = maxfollowers, minfollowers = minfollowers, enforceclarifai = enforceclarifai, enforcebanned = enforcebanned, subscribedcategories = subscribedcategories)
            insert.save()

            return redirect('/graph/editpreferences')

    context = {
        'form': form,
        'user': user,
        'info': info,
        'getcategories': getcategories,
    }
    return render(request, 'graph/editpreferences.html', context)



class InstaHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = InstaHistory
        fields= ('accountuser', 'uploads', 'totalfollowers', 'totalfollows', 'date')

class history_data_view(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        user = request.user
        hist = InstaHistory.objects.filter(accountuser = user).order_by('date')
        for x in hist:
            x.date = formats.date_format(x.date, "SHORT_DATETIME_FORMAT")
        serializer = InstaHistorySerializer(hist, many=True)
        dataSerialized = serializer.data

        data = {
            'user': str(request.user),  # `django.contrib.auth.User` instance.
            'auth': str(request.auth), 
            'followerdata': dataSerialized
        }
        return Response(data)


class FeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikeHistory
        fields= ('accountuser', 'username', 'link', 'date')

class heart_feed_view(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    def get(self, request, format=None):
        user = request.user
        feed = LikeHistory.objects.filter(accountuser = user).order_by('-date')
        for x in feed:
            #x.link = '<a href="'  + (x.link) +  '"> </a> '
            #<a href=""></a>
            x.date = formats.date_format(x.date, "SHORT_DATETIME_FORMAT")
            

        serializer = FeedSerializer(feed, many=True)
        dataSerialized = serializer.data

        data = {
            'user': str(request.user),
            'auth': str(request.auth),
            'heartdata': dataSerialized
        }
        return Response(data)








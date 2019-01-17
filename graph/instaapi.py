from django.conf import settings
import os
import requests
import datetime
from datetime import timedelta
import time


class instaStats(object):
    def returnStats(self, x, y):
        #for Insta official API
        clientid = x
        ACCESS_TOKEN = y
        PARAMSGeneral = {'ACCESS_TOKEN': ACCESS_TOKEN}
        URLGeneral = "https://api.instagram.com/v1/users/self/?access_token="+ACCESS_TOKEN
        r1 = requests.get(url = URLGeneral, params = PARAMSGeneral)
        data1 = r1.json()
        dataGeneral = data1['data']
        return data1

class recentStats(object):
    def recentMediaInfo (self, token, count):
        #for Insta official API - most recent upload
        ACCESS_TOKEN = token
        PARAMSRecent = {'ACCESS_TOKEN': token, 'count': count}
        URLRecent = "https://api.instagram.com/v1/users/self/media/recent/?access_token="+ACCESS_TOKEN
        r2 = requests.get(url = URLRecent, params = PARAMSRecent)
        data2 = r2.json()
        dataRecent = data2['data']
        return data2

class timeCompare(object):
    def epochtime(x):
        returntime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(x))
        return returntime

    def uploadTime(lastUploadTime):
        currentTime = int(time.time())
        differenceTime = currentTime - lastUploadTime
        return differenceTime















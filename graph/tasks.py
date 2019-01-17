from __future__ import absolute_import, unicode_literals

from celery import task
from celery.schedules import crontab


from django.conf import settings
import os
import requests
import datetime
from datetime import timedelta, datetime
import time
from time import sleep
from random import randint
import pytz

import psycopg2
from django.contrib.auth.models import User
from graph.models import UserInfo, LikingPreferences, InstaCategories, LikeHistory, InstaHistory
from accounts.models import Subscription
from graph.instaapi import *

#selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from clarifai.rest import ClarifaiApp, Image as ClImage

#headless chromedriver config to run on local server
#options = Options()
#options.add_argument('--headless')
#options.add_argument('--disable-gpu')

#headless chromedriver config to run on cloud server
#chrome_bin = os.environ.get('GOOGLE_CHROME_SHIM', None)
#chrome_options = Options()
#chrome_options.binary_location = chrome_bin
#chrome_options.add_argument('--disable-gpu')
#chrome_options.add_argument('--no-sandbox')

#start session in chrome on local server
#if want to use headless
#browser = webdriver.Chrome('./assets/chromedriver', chrome_options=options)
#if want to see chrome
#browser = webdriver.Chrome('./assets/chromedriver')
##browser = webdriver.Chrome(executable_path='C:\webdriver\chromedriver.exe')

#start session in chrome on CLOUD SERVER
#browser = webdriver.Chrome(executable_path="chromedriver", chrome_options=chrome_options)

#starting database with postgreSQL - ON LOCAL COMPUTER
conn = psycopg2.connect(host="localhost", database="instagram", user="postgres", password="lovelife24")
c = conn.cursor()
#print("connected to db")

#starting database with postgreSQL - ON HEROKU
#DATABASE_URL = os.environ['postgresql-tapered-55694']
#conn = psycopg2.connect(DATABASE_URL, sslmode='require')
#c = conn.cursor()
#print("connected to db")

#used in most functions - 15 second delay if can't load
delay = 15

hourLikeCount = 0
totalLikeCount = 0
consecCount = 0
picCount = 0 
i = 0




def heartPic(browser, getUserInfo, user_name):
    #finding hearts when on picture - ready to use. 
    hearts = browser.find_elements_by_class_name('coreSpriteHeartOpen')

    #print(len(hearts))
    sleep(5)
    ActionChains(browser).move_to_element(hearts[0]).click().perform()
    
    print("liked photo")
    sleep(5)

    global hourLikeCount 
    hourLikeCount +=1

    global totalLikeCount
    totalLikeCount +=1

    url = browser.current_url
    print(url)

    #INSERT USERNAME AND TIME TO DATABASE using postgreSQL
    insert = LikeHistory(accountuser = getUserInfo.accountuser, username = user_name, link = url, date = datetime.datetime.today())
    insert.save()



def clarifai(browser, getUserInfo, myPreferences, user_name):
    if myPreferences.enforceclarifai == True:

        print('api clarifai')
        #need img_link
        clarifai_api = ClarifaiApp(api_key='a88172a02f3e4036b5b13bdee391e7f3')
        img_link = browser.find_element_by_xpath('//img[@class = "FFVAD"]') \
            .get_attribute('src')

        print(img_link)

        #general model
        #model = clarifai_api.models.get('general-v1.3')

        #nsfw model
        model = clarifai_api.models.get('e9576d86d2004ed1a38ba0cf39ecb4b1')

        image = ClImage(url=img_link)
        #only predicts image, not videos
        result = model.predict([image])
        #print(result)

        sfwValue = float(result['outputs'][0]['data']['concepts'][0]['value'])
        print(sfwValue)

        if sfwValue >= 0.80:
            print("passed clarifai")
            
            heartPic(browser, getUserInfo, user_name)
        else:
            print("failed clarifai")

    elif myPreferences.enfoceclarifai == False:
        #go ahead and like pic regardless
        heartPic(browser, getUserInfo, user_name)


def tagsAndComments(browser, getUserInfo, myPreferences, listofbannedhashtags, user_name):
    #go back to most recent pic
    main_elem = browser.find_elements_by_class_name('v1Nh3')[0]
    link_elems1 = main_elem.find_elements_by_tag_name('a')
    total_links1 = len(link_elems1)
    print("Total loaded pics on profile ", total_links1)
    ActionChains(browser).move_to_element(link_elems1[0]).click().perform()
    sleep(10)


    if myPreferences.enforcebanned == True:
        #load user hashtags
        hashtags = browser.find_element_by_class_name('C4VMK').text
        sleep(5)

        hashtagPara = hashtags.replace(",", "").replace("#", "").replace(".","").replace("-","").replace("@","").replace("_","").replace("|","")
        #print(len(hashtagPara))
        #print(hashtagPara)
        sleep(5)
        
        hashtagWords = hashtagPara.split()
        print(hashtagWords)

        #if no comment, will be out of range
        try:  
            hashtagsComment = browser.find_elements_by_class_name('CV4MK')[1].text
            #hasht = hashtags.find_elements_by_tag_name('a').text
            sleep(5)
            hashtagParaComment = hashtagsComment.replace(",", "").replace("#", "").replace(".","").replace("-","").replace("@","").replace("_","").replace("|","")
            #print(len(hashtagParaComment))
            #print(hashtagParaComment)
            sleep(5)
            hashtagWordsComment = hashtagParaComment.split()
            #print(hashtagWordsComment)
            isComment = True
            print("first comment?", isComment)

        except NoSuchElementException:
            isComment = False
            print("first comment?", isComment)
            #try to continue anyway

        except IndexError:
            isComment = False
            print("first comment?", isComment)
            #try to continue anyway

        #if there is a first comment
        if isComment == True:
            if (any(x in hashtagWords for x in listofbannedhashtags)) and (any(x in hashtagWordsComment for x in listofbannedhashtags)):
                print("failed hashtag criteria")

            else:
                print("passed hashtag criteria")

                clarifai(browser, getUserInfo, myPreferences, user_name)

        #if no first comment
        elif isComment == False:
            if any(x in hashtagWords for x in listofbannedhashtags):
                print("failed hashtag criteria")

            else:
                print("passed hashtag criteria")

                clarifai(browser, getUserInfo, myPreferences, user_name)
    elif myPreferences.enforcebanned == False:
        print('skipping banned words')
        #move on to enforce clarifai if true
        clarifai(browser, getUserInfo, myPreferences, user_name)



def toUserProfile(browser, getUserInfo, myPreferences, sleepTimeout, listofbannedhashtags, user_name):
    #make sure page has loaded
    try:
        #OK for now. any class will do
        usernamePage = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.CLASS_NAME, '-nal3')))
        print("Navigated to users page")

    except TimeoutException:
        print("Loading users took too much time")
        sleep(10)

    except:
        print('not loading correctly')

    #like criteria setup
    minPosts = myPreferences.minposts     
    maxFollowers = myPreferences.maxfollowers
    minFollowings = myPreferences.minfollowers

    #post count
    posts = browser.find_elements_by_class_name('g47SY')[0].text
    sleep(3)
    postCount = int(posts.replace(",",""))
    print("posts ", postCount)
    sleep(1)

    #followers
    followers = browser.find_elements_by_class_name('g47SY')[1]
    sleep(1)
    followerTitle = followers.get_attribute('title')
    sleep(1)
    followerCount = int(followerTitle.replace(",",""))
    print("Followers ", followerCount)
    sleep(1)

    #follows
    follows = browser.find_elements_by_class_name('g47SY')[2].text
    sleep(1)
    followingCount = int(follows.replace(",",""))
    print("Following ", followingCount)
    sleep(3)

    if ((postCount >= minPosts) and (followerCount <= maxFollowers) and (followingCount >= minFollowings)):
        #go back to most recent pic posted and like it if the tags are ok
        print("passed post/follow criteria")

        #need - running count
        tagsAndComments(browser, getUserInfo, myPreferences, listofbannedhashtags, user_name)

    else:
        print("failed post/follow criteria")
        #return to loop without liking picture

    global picCount 
    picCount +=1

    print("Total looks this round: ", picCount)
    sleep(sleepTimeout)  



def startLoop(browser, getUserInfo, myPreferences, listofcategoriestolike, listofbannedhashtags):

    likesperhour = myPreferences.likesperhour
    conseclikes = myPreferences.consecutivehours
    likesperday = myPreferences.likesperday

    catLength = len(listofcategoriestolike)
    print(catLength)

    #for i in range(len(listofcategoriestolike)):
    global consecCount
    while consecCount <= conseclikes:  
        #begin tracking time to sleep till next hour starts
        
        global totalLikeCount
        if totalLikeCount < likesperday:
            startTime = time.time()
            global hourLikeCount
            if hourLikeCount < likesperhour: 
                global i 
                if i >= catLength:
                    i = 0
                elif i < catLength:
                    sleepTimeout = randint(10, 31)
                    print("hashtag", listofcategoriestolike[i], "+ sleep seconds ", sleepTimeout)

                    browser.get('https://www.instagram.com/explore/tags/'
                        + (listofcategoriestolike[1:] if listofcategoriestolike[:1] == '#' else listofcategoriestolike[i]))

                    #try to load hashtag page
                    try:
                        #explorePage = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.CLASS_NAME, '_havey')))
                        explorePage = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.TAG_NAME, "h2")))
                        print("Navigated to explore tags page")

                    except TimeoutException:
                        print("Loading tags took too much time")
                        sleep(10)

                    #skip top posts
                    main_elemSkipTop = browser.find_element_by_xpath('//main/article/div[2]')

                    browser.execute_script(
                        "window.scrollTo(0, document.body.scrollHeight);")
                    sleep(5)
                    print("scrolled down")

                    #go to most recent
                    link_elems = main_elemSkipTop.find_elements_by_tag_name('a')
                    total_links = len(link_elems)
                    #should have 24 links to choose from
                    print("Total loaded pics (not including top) ", total_links)
                    sleep(5)

                    #between 0 and 24
                    chooseRandomPic = randint(0, (total_links - 1))
                    print("Random order # ", chooseRandomPic)

                    #click on first a 
                    ActionChains(browser).move_to_element(link_elems[chooseRandomPic]).click().perform()
                    sleep(10)

                    #get usrname of post
                    postUser = browser.find_element_by_class_name('nJAzx').text
                    sleep(3)
                    #print(len(postuser))
                    user_name = postUser
                    print("Username: ", user_name)
                    sleep(3)

                    #go to account
                    userLink = 'https://www.instagram.com/' + user_name
                    browser.get(userLink)

                    #looks at user account
                    toUserProfile(browser, getUserInfo, myPreferences, sleepTimeout, listofbannedhashtags, user_name)
                    
                    i += 1   
                    print('i: ')  
                    print(i) 
                    print('hour like count: ')
                    print(hourLikeCount)
                    
                    print('total like count')
                    print(totalLikeCount)
            else:
                print('sleeping till hour is up')
                endTime = time.time()
                timeDif = endTime - startTime
                print(timeDif)
                #sleep until hour is complete
                hour = 60 * 60
                
                consecCount += 1

                hourLikeCount = 0
                if timeDif > hour:
                    sleep(hour - (timeDif - hour))
                    print((hour - (timeDif - hour))/60)
                elif timeDif < hour:     
                    sleep(hour - timeDif)
                    print((hour - timeDif)/60)
        else:
            return
               
                

            
            

            
            



def sessionLogin(getUserInfo, myPreferences, listofcategoriestolike, listofbannedhashtags):
    browser = webdriver.Chrome(executable_path='C:\webdriver\chromedriver.exe')
    #navigate to a webpage
    browser.get('https://www.instagram.com/accounts/login/')

    try:
        #loginPage = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.CLASS_NAME, '_ev9xl')))
        loginPage = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.XPATH, "//input[@name='username']")))
        print("Navigated to login page")

    except TimeoutException:
        print("Loading login took too much time")
        sleep(10)
    except:
        print('error finding loading indication')

    #find form inputs username
    input_username = browser.find_elements_by_xpath("//input[@name='username']")

    #enter username
    ActionChains(browser).move_to_element(input_username[0]). \
        click().send_keys(getUserInfo.instauser).perform()
    sleep(3)

    #find form input password
    input_password = browser.find_elements_by_xpath("//input[@name='password']")

    #enter password
    ActionChains(browser).move_to_element(input_password[0]). \
        click().send_keys(getUserInfo.instapass).perform()
    sleep(3)

    #find login button
    #login_button = browser.find_elements_by_xpath("//form/span/button[text()='Log in']")
    login_button = browser.find_elements_by_xpath("//*[@id='react-root']/section/main/div/article/div/div[1]/div/form/div[3]/button")
    #click log in button
    ActionChains(browser).move_to_element(login_button[0]).click().perform()
    sleep(10)

    if browser.current_url == 'https://www.instagram.com/':

        #scrolling
        #find body
        body_elem = browser.find_element_by_tag_name('body')
        #load new images by going up and down
        #for _ in range(3):
            #body_elem.send_keys(Keys.END)
            #sleep(5)
            #body_elem.send_keys(Keys.HOME)
            #sleep(5)

        #start searching for hashtags
        startLoop(browser, getUserInfo, myPreferences, listofcategoriestolike, listofbannedhashtags)

    elif browser.current_url == 'https://www.instagram.com/accounts/login/':
        print('incorrect passweord or username')
    else:
        print('problem loggin')
        print(browser.current_url)


    #close conncetion to db
    #c.close()
    #conn.close()
    browser.close()


def loadCategories(getUserInfo):
    try: 
        myPreferences = LikingPreferences.objects.get(accountuser = getUserInfo.accountuser)
        myCategories = myPreferences.subscribedcategories
        enforceBan = myPreferences.enforcebanned

        cats = InstaCategories.objects.all()

        listofcategoriestolike = []
        listofbannedhashtags = []

        if enforceBan == True:
            for x in cats:
                if x.catname == 'BANNED':
                    #print(x.catarray)
                    listofbannedhashtags = x.catarray

        for x in cats:
            for y in myCategories:
                if x.catname == y:
                    listofcategoriestolike.extend(x.catarray)
    
        #combined list of all hashtags to like from categories
        #print(listofcategoriestolike)
        #print(listofbannedhashtags)
        print('passed load cats')
   
    except:
        print('error loading cats')

    sessionLogin(getUserInfo, myPreferences, listofcategoriestolike, listofbannedhashtags)

    

@task()
def checkTime():
    #make sure there is valid subscriptions in db
    if Subscription.objects.filter(active=True, isrunning=False).count() > 0:
        #for each row in db
        for startLoop in Subscription.objects.filter(active=True, isrunning=False):
            #if already running, don't do anything - in case of celery overlap
            if startLoop.isrunning == True:
                print('do nothing - already running')
            else:
                #set to true so as to not overlap tasks then at end change to false
                startLoop.isrunning = True
                startLoop.save()

                getUserInfo = UserInfo.objects.get(accountuser = startLoop.accountuser)
                #check to make sure subscription is active
                if startLoop.active == True:
                    #upload the stats of the last media uploaded
                    instarecentmedia = recentStats()
                    statrecent = instarecentmedia.recentMediaInfo(getUserInfo.accesstoken, 1)
                    dataRecent = statrecent['data']
                    dataRecent = dataRecent[0]
                    #compare time
                    checktime = int(dataRecent['created_time'])            
                    compareTime = timeCompare()
                    dataRecentTime = timeCompare.epochtime(checktime)

                    #comparing current time to last upload time
                    uploadTimeDifference = timeCompare.uploadTime(checktime)
                    #print(uploadTimeDifference)

                    currentTime = int(time.time())
                    #print(currentTime)
                    try: 
                        likeTime = LikingPreferences.objects.get(accountuser = getUserInfo.accountuser)
                        likeTimeToSecs = likeTime.consecutivehours * 60 * 60
                        #print(likeTimeToSecs)
                    except: 
                        likeTime = 0
                        likeTimeToSecs = 0

                    #flip this when ready for real
                    if currentTime >= uploadTimeDifference + likeTimeToSecs:
                        #uploaded pic within however many hours specified on preferences
                        print('start')
                        loadCategories(getUserInfo)
                
                    else:
                        print("uploaded over specified hours ago")
                else:
                    print('not a subscriber')
                #when done, tell celery that program is no longer running on account
                startLoop.isrunning  = False
                startLoop.save()
    else: 
        print('no active subscriptions')


@task()
def updateStat():
    for getUserInfo in UserInfo.objects.all():
        instamedia = instaStats()
        statinfo = instamedia.returnStats(getUserInfo.clientid, getUserInfo.accesstoken)
        dataGeneral = statinfo['data']
        mediaGeneral = dataGeneral['counts']
        print(mediaGeneral['media'])
        
        insert = InstaHistory(accountuser = getUserInfo.accountuser, uploads = mediaGeneral['media'], totalfollowers = mediaGeneral['follows'], totalfollows = mediaGeneral['followed_by'], date = datetime.datetime.today())
        insert.save()

@task()
def updateSubscribers():
    for getUserInfo in Subscription.objects.all():
        utc = pytz.UTC
        currentTime = utc.localize(datetime.datetime.now())
        #active sub
        if getUserInfo.subend >= currentTime:
            if getUserInfo.active == True:
                print('stay active')
            elif getUserInfo.active == False:
                getUserInfo.active = True
                getUserInfo.save()
                print('change false to true')
        #inactive sub
        elif getUserInfo.subend < currentTime:
            if getUserInfo.active == False:
                print('stay false')
            elif getUserInfo.active == True:
                getUserInfo.active = False
                getUserInfo.save()
                print('change true to false')
        
        



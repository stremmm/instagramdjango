from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings


from django.contrib.auth.models import User
#from django.utils.text import slugify
from django.contrib.postgres.fields import ArrayField



class InstaCategories(models.Model):
    catname = models.CharField(max_length=100, blank=False, null=False)
    catarray = ArrayField(models.CharField(max_length=80, blank=False), size=80)

    class Meta:
        managed=True
        db_table = 'InstaCategories'
        verbose_name_plural = 'InstaCategories'

    def __str__(self):
        return self.catname

class UserInfo(models.Model):
    accountuser = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    instauser = models.CharField(max_length=100, blank=False, null=False)
    instapass = models.TextField(blank=False, null=False)
    clientid = models.CharField(max_length=100, blank=False, null=False)
    accesstoken = models.CharField(max_length=100, blank=False, null=False)
    startdate = models.DateTimeField(null=False, blank=False)
    


    def __str__(self):
        return self.instauser
    
    class Meta:
        managed = True
        db_table = 'UserInfo'
        verbose_name_plural = 'UserInfo'

class LikingPreferences(models.Model):
    BOOL_CHOICES = (
        (True, 'Yes'),
        (False, 'No'),
    )
    accountuser = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    #cutoff at 60/hr. and 450/day.
    likesperhour = models.IntegerField(blank=False, null=False, default=60,
        validators=[
            MaxValueValidator(60),
            MinValueValidator(1)
        ])
    consecutivehours = models.IntegerField(blank=False, null=False, default=7, 
        validators=[
            MaxValueValidator(24),
            MinValueValidator(1)
        ])
    likesperday = models.IntegerField(blank=False, null=False, default=400,
        validators=[
            MaxValueValidator(450),
            MinValueValidator(1)
        ])
    minposts = models.IntegerField(blank=False, null=False, default=5,
        validators=[
            MaxValueValidator(50),
            MinValueValidator(0)
        ])
    maxfollowers = models.IntegerField(blank=False, null=False, default=400,
        validators=[
            MaxValueValidator(10000),
            MinValueValidator(1)
        ])
    minfollowers = models.IntegerField(blank=False, null=False, default=400,
        validators=[
            MaxValueValidator(10000),
            MinValueValidator(1)
        ])
    enforceclarifai = models.BooleanField(choices = BOOL_CHOICES)
    enforcebanned = models.BooleanField(choices = BOOL_CHOICES)
    subscribedcategories = ArrayField(models.CharField(max_length=50, blank=False), size=15)
    


    #def __str__(self):
        #return self.subscribedcategories

    class Meta:
        managed=True
        db_table = 'LikingPreferences'
        verbose_name_plural = 'LikingPreferences'

class InstaHistory(models.Model):
    accountuser = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    uploads = models.IntegerField(null=False, blank=False)
    totalfollowers = models.IntegerField(null=False, blank=False)
    totalfollows = models.IntegerField(null=False, blank=False)
    date = models.DateTimeField(null=False, blank=False)

    class Meta:
        managed=True
        db_table = 'InstaHistory'
        verbose_name_plural = 'InstaHistory'

    def dateFixed(self):
        return self.date.strftime('%b, %d, %Y')


class LikeHistory(models.Model):
    accountuser = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    username = models.CharField(max_length=100, blank=False, null=False)
    link = models.TextField(null=False, blank=False)
    date = models.DateTimeField(null=False, blank=False)


    class Meta:
        managed=True
        db_table = 'LikeHistory'
        verbose_name_plural = 'LikeHistory'

    def __str__(self):
        return self.username





    








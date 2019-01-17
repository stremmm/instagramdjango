from django import forms
from django.contrib.auth.models import User

from django.db import models
from django.forms import ModelForm
from graph.models import *

class userinfo_Form(ModelForm):
    instauser = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"placeholder": "Instagram Username"}))
    instapass = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"placeholder": "Instagram Password"}))
    clientid = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"placeholder": "Instagram API Client ID"}))
    accesstoken = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"placeholder": "Instagram API Access Token"}))

    class Meta:
        model = UserInfo
        fields=['instauser', 'instapass', 'clientid', 'accesstoken']

class likingpreferences_Form(ModelForm):
    CHOICES = (
        ('FOOD', 'FOOD'),
        ('HEALTH', 'HEALTH'),
        ('FITNESS', 'FITNESS'),
        ('MODELS', 'MODELS'),
        ('FASHION', 'FASHION'),
        ('BEAUTY', 'BEAUTY'),
        ('PHOTOGRAPHY', 'PHOTOGRAPHY'),
        ('ART/DESIGN', 'ART/DESIGN'),
        ('HOME DESIGN', 'HOME DESIGN'),
        ('LUXURY/BRANDS', 'LUXURY/BRANDS'),
        ('TRAVEL', 'TRAVEL'),
        ('MUSIC', 'MUSIC'),
    )
    
    likesperhour = forms.IntegerField(label="Likes Per Hour", widget=forms.TextInput(attrs={"placeholder": "Max 350"}))
    consecutivehours = forms.IntegerField(label="Consecutive Hours", widget=forms.TextInput(attrs={"placeholder": "Max 24"}))
    likesperday = forms.IntegerField(label="Likes Per Day", widget=forms.TextInput(attrs={"placeholder": "Max 450"}))
    minposts = forms.IntegerField(label="Minimum Posts", widget=forms.TextInput(attrs={"placeholder": "Max 50"}))
    maxfollowers = forms.IntegerField(label="Maximum Followers", widget=forms.TextInput(attrs={"placeholder": "Max 10000"}))
    minfollowers = forms.IntegerField(label="Minimum Follows", widget=forms.TextInput(attrs={"placeholder": "Min 1"}))
    enforceclarifai = forms.BooleanField(label="Run Clarifai")
    enforcebanned = forms.BooleanField(label="Enforce Banned Hashtags")
    subscribedcategories = forms.MultipleChoiceField(label="Categories", choices=CHOICES, widget=forms.CheckboxSelectMultiple())

    class Meta:
        model = LikingPreferences
        fields=['likesperhour', 'consecutivehours', 'likesperday', 'minposts', 'maxfollowers', 'minfollowers', 'enforceclarifai', 'enforcebanned', 'subscribedcategories']

class deletehistory_form(forms.Form):
    acctuser = forms.IntegerField(widget=forms.HiddenInput())

    class Meta:
        fields=['acctuser',]
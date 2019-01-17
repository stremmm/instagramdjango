from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.urls import reverse

from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.contrib import messages
from django.contrib.auth import login, authenticate

from accounts.forms import *
from accounts.models import *
from graph.models import UserInfo, LikingPreferences

import random
import datetime
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
def signUp_view(request):
    if request.method == 'POST':
        form = Signup_Form(request.POST or None)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            to_user = form.cleaned_data.get('username')
            to_email = form.cleaned_data.get('email')

            current_site = get_current_site(request)
            mail_subject = 'Activate your Account'
            message = render_to_string('acc_activate_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user),
            })

            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )

            print('sent email conf')
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration.')
        else:
            print('errors')
    else:
        form = Signup_Form()
    return render(request, 'accounts/signup.html', {'form': form})

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return HttpResponse('Thank you for your email confirmation. Now you can login to your account.')
    else:
        return HttpResponse('Activation link is invalid!')

def subscription_view(request):
    user = request.user
    sub = None
    instainfo = None
    instapref = None
    try: 
        sub = Subscription.objects.get(accountuser = user)
    except:
        print('error sub')

    try:
        instainfo = UserInfo.objects.get(accountuser = user)
    except:
        print('error')

    try:
        instapref = LikingPreferences.objects.get(accountuser = user)
    except:
        print('error')

    startform = startsub_form(request.POST or None)



    if request.method == 'POST':
        if request.POST['action']=='Start Sub Via Paypal':
            nodupe = False
            while nodupe is False:
                try:
                    subnumber = random.randint(1000000, 9000000)
                    subnumber_query = Subscription.objects.get(ordernumber = subnumber)
                    nodupe=False
                except ObjectDoesNotExist:
                    print(subnumber)
                    nodupe=True

            #add to subscription database here
            try:
                #if already in db
                update = Subscription.objects.get(accountuser = user)
                print(update.accountuser.username)
                update.accountuser = user
                update.ordernumber = subnumber
                update.substart = datetime.datetime.today()
                update.subend = datetime.datetime.today()
                update.active = False
                update.isrunning = False
                update.save()
            except:
                insert = Subscription(accountuser = user, ordernumber = subnumber, substart = datetime.datetime.today(), subend = datetime.datetime.today(), active = False, isrunning = False)
                insert.save()
                print('didnt find previous sub, so making new one in db')

            


            return redirect(reverse('payment:process'))


    context = {
        'sub': sub,
        'instainfo': instainfo,
        'instapref': instapref,
        'startform': startform,
    }

    return render(request, 'accounts/subscription.html', context)


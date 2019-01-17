from django.shortcuts import get_object_or_404
from django.core.mail import EmailMessage
from django.conf import settings
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received
from accounts.models import Subscription

import datetime


def payment_notification(sender, **kwargs):
    ipn_obj = sender
    #check for buy now
    if ipn_obj.txn_type == 'web_accept':
        if ipn_obj.payment_status == ST_PP_COMPLETED:
            order = get_object_or_404(Subscription, ordernumber = ipn_obj.invoice)

            order.subend = order.substart + datetime.timedelta(+30)
            order.active = True
            order.save()
            print('buy now')
    #subscribe sign up?
    elif ipn_obj.txn_type == 'subscr_signup':
        print('signup')
    #subscribe payment
    elif ipn_obj.txn_type == 'subscr_payment':
        print('subscribe payment')
        order = get_object_or_404(Subscription, ordernumber = ipn_obj.invoice)
        order.subend = order.substart + datetime.timedelta(+30)
        order.active = True
        order.save()

    elif ipn_obj.txn_type == "subscr_cancel":
        print('subscribe cancel')

 








valid_ipn_received.connect(payment_notification)
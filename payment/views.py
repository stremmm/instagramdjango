
# Create your views here.
from django.conf import settings
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from paypal.standard.forms import PayPalPaymentsForm
from django.views.decorators.csrf import csrf_exempt
from accounts.models import Subscription
from django.contrib.auth.models import User

@csrf_exempt
def payment_done(request):
    return render(request, 'payment/done.html')

@csrf_exempt
def payment_canceled(request):
    return render(request, 'payment/canceled.html')

def payment_process(request):
    user = request.user
    order = get_object_or_404(Subscription, accountuser = user)
    host= request.get_host()

    paypal_dict = {
        "cmd": "_xclick-subscriptions",
        "business": settings.PAYPAL_RECEIVER_EMAIL,
        
        "a3": "9.99",                      # monthly price
        "p3": 30,                           # duration of each unit (depends on unit)
        "t3": "D",                         # duration unit ("M for Month")
        "src": "1",                        # make payments recur
        "sra": "1",                        # reattempt payment on payment error
        "no_note": "1",                    # remove extra notes (optional)
        "item_name": "Order {}".format(order.ordernumber),
        "invoice": str(order.ordernumber),
        "currency_code": "USD",
        "notify_url": "http://{}{}".format(host, reverse('paypal-ipn')),
        "return": "http://{}{}".format(host, reverse('payment:done')),
        "cancel_return": "http://{}{}".format(host, reverse('payment:canceled')),
        }

    # paypal_dict = {
    #     "business": settings.PAYPAL_RECEIVER_EMAIL,
    #     "amount": "9.99",
    #     "item_name": "Order {}".format(order.ordernumber),
    #     "invoice": str(order.ordernumber),
    #     "notify_url": "http://{}{}".format(host, reverse('paypal-ipn')),
    #     "return": "http://{}{}".format(host, reverse('payment:done')),
    #     "cancel_return": "http://{}{}".format(host, reverse('payment:canceled')),
    #     #"custom": "premium_plan",  # Custom command to correlate to some function later (optional)
    # }

    # Create the instance.
    form = PayPalPaymentsForm(initial=paypal_dict, button_type="subscribe")
    #form = PayPalPaymentsForm(initial=paypal_dict)

    # Output the button.
    return render(request, 'payment/process.html', {'order': order,
                                            'form': form})


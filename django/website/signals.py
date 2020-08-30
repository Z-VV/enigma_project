from paypal.standard.ipn.signals import valid_ipn_received
from django.dispatch import receiver
from paypal.standard.models import ST_PP_COMPLETED
from django.core.mail import EmailMessage
from django.contrib.auth.models import User
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
import os
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from email.mime.text import MIMEText
import base64
from .gmail_send import compose_and_send
from datetime import datetime,timezone
from rest_framework.authtoken.models import Token



@receiver(valid_ipn_received)
def ipn_receiver(sender, **kwargs):

    ipn_obj = sender
    unpacked_data = ipn_obj.custom.split('|')
    for x in range(3):
        print(unpacked_data)

    # check for Buy Now IPN
    if ipn_obj.txn_type == 'web_accept':
        for x in range(10):
            print('web_accept')

        if ipn_obj.payment_status == ST_PP_COMPLETED:
            # payment was successful
            print('great!')
            order = get_object_or_404(Order, id=ipn_obj.invoice)

            if order.get_total_cost() == ipn_obj.mc_gross:
                # mark the order as paid
                order.paid = True
                order.save()

    # check for subscription signup IPN
    elif ipn_obj.txn_type == "subscr_signup":
        sub_cycle =''

        for x in range(3):
            print('subscr_singup')
            print(type(ipn_obj.custom))


        id = int(unpacked_data[1])
        user = User.objects.get(id=id)
        email = user.email

        if unpacked_data[2] == 'week':
            sub_cycle = 'weekly'

        if unpacked_data[2] == 'month':
            sub_cycle = 'monthly'

        message_text = 'Hello '+user.first_name+' .\nThank you for your Subscription.\nWe are processing your payment and will activate your '\
                       +sub_cycle+' subscription.\nPlease wait for confirmation email.\n'+\
            'If you have any questions we are here to help.\nBest regards,\nCustomer support team.'
        compose_and_send('Enigma-Lab', email, 'Enigma-Lab customer support team', message_text)

    # check for subscription payment IPN
    elif ipn_obj.txn_type == "subscr_payment":
        for x in range(10):
            print('subscr_payment')
            print(ipn_obj.custom)

        # get user id and extend the subscription
        mc_gross = ipn_obj.mc_gross
        token = '0'

        id = int(unpacked_data[1])
        user = User.objects.get(id=id)
        if unpacked_data[2] == 'week':
            user.profile.week_payment_date = datetime.now(timezone.utc)
            user.profile.week_subscription = True
            user.save()
            if len(Token.objects.filter(user=user)) != 0 and not user.is_superuser:
                user.auth_token.delete()
                token = Token.objects.create(user=user)
            else:
                token = Token.objects.create(user=user)


        if unpacked_data[2] == 'month':
            user.profile.month_payment_date = datetime.now(timezone.utc)
            user.profile.month_subscription = True
            user.save()
            if len(Token.objects.filter(user=user)) != 0 and not user.is_superuser:
                user.auth_token.delete()
                token = Token.objects.create(user=user)
            else:
                token = Token.objects.create(user=user)


        email = user.email
        print(user)

        message_text = 'Hello ' + user.first_name + ' .\nThank you for your Subscription payment.' \
                                                    '\nYour PayPal account have been charged '+str(mc_gross) + \
            '\nand your active Token is: '+ str(token)+'\n'+\
                       'If you have any questions we are here to help.\nBest regards,\nCustomer support team.'
        compose_and_send('Enigma-lab',email,'Enigma-Lab customer support team',message_text)


    # check for failed subscription payment IPN
    elif ipn_obj.txn_type == "subscr_failed":
        for x in range(10):
            print('subscr_failed')
        pass


    # check for subscription cancellation IPN
    elif ipn_obj.txn_type == "subscr_cancel":
        pass






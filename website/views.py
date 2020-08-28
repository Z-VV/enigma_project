from django.shortcuts import render,redirect,reverse
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm
from django.contrib.auth.forms import AuthenticationForm
from .models import Message
from django.db import IntegrityError
from decimal import Decimal
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from paypal.standard.ipn import models
from rest_framework.authtoken.models import Token
from django.apps import apps
from datetime import timedelta,datetime,timezone
import mimetypes
from django.http import HttpResponse
from django.core.files import File
import time
from .gmail_send import gmail_first_message
from ipware import get_client_ip
import os


# Create your views here.

def index(request):
    ip, is_routable = get_client_ip(request)

    print(ip, is_routable)
    if request.user.is_authenticated:
        p, is_routable = get_client_ip(request)

        for x in range(10):
            print(p,is_routable)

        return redirect('logged/')

    if request.method == 'POST':
        if 'signup_form' in request.POST :
            form = SignUpForm(request.POST)
            print(form)
            if form.is_valid():

                form.save()

                username = form.cleaned_data.get('username')

                password = form.cleaned_data.get('password1')
                user = authenticate(username=username, password=password)

                login(request, user)
                return redirect('logged/')
            else:
                return render(request, 'pop_account_exists.html', {'form': form})

        if 'signin_form' in request.POST:
            username = request.POST['username']
            password = request.POST['password1']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('logged/')
            else:
                form = AuthenticationForm(request.POST)
                return render(request, 'pop_index.html',  {'form':form})

        if 'message_form' in request.POST:
            if request.POST.get('name') and request.POST.get('email'):
                try:
                    post = Message()
                    post.name = request.POST.get('name')
                    post.email = request.POST.get('email')
                    post.text = request.POST.get('text')
                    print(post.name,post.email,post.text)
                    post.save()

                    return render(request, 'pop_after_message.html')

                except IntegrityError:
                    return render(request,'pop_message_error.html')

    else:
        form = SignUpForm()
        return render(request, 'pop_index.html', {'form': form})


def logged(request):

    if request.method == 'POST':
        if 'logout_form' in request.POST:
            logout(request)
            return redirect(index)

        if 'message_form' in request.POST:
            if request.POST.get('name') and request.POST.get('email'):
                try:
                    post = Message()
                    post.name = request.POST.get('name')
                    post.email = request.POST.get('email')
                    post.text = request.POST.get('text')
                    print(post.name,post.email,post.text)
                    post.save()
                    return render(request, 'pop_after_message.html')

                except IntegrityError:
                    return render(request,'pop_message_error.html')

        if 'app_download' in request.POST:
            user_model_info = user_info_get(request.user.id)
            if user_model_info['app_download'] == False:
                return redirect('download/')

            if user_model_info['app_download'] == True:
                user_id = request.user.id
                user_model_info = user_info_get(user_id)
                subscription_forms_list = process_subscription(request)
                name = request.user.username.capitalize()
                print(user_model_info['app_download'])
                return render(request, 'pop_logged.html', {'name': name, 'form_week': subscription_forms_list[0],
                                                       'form_month': subscription_forms_list[1],
                                                       'user_model_info': user_model_info})

    else:
        user_id = request.user.id
        user_model_info = user_info_get(user_id)
        subscription_forms_list = process_subscription(request)
        name = request.user.username.capitalize()
        print(user_model_info['app_download'])
        return render(request,'pop_logged.html', {'name': name ,'form_week':subscription_forms_list[0],
                                                  'form_month':subscription_forms_list[1],'user_model_info':user_model_info})

def download_file(request):
    fl_path = 'C:/Users\\master\\Desktop\\myApp\\KILL EXE\\unknown_cmd_working.exe'

    filename = 'money_app.exe'

    fl = open(fl_path, 'rb')
    mime_type, _ = mimetypes.guess_type(fl_path)
    response = HttpResponse(fl, content_type=mime_type)
    response['Content-Disposition'] = "attachment; filename=%s" % filename

    user_id = request.user.id
    user = User.objects.get(pk=user_id)
    user.profile.app_download = True
    user.profile.app_download_time = datetime.now(timezone.utc)
    trial_token = Token.objects.create(user=user)
    user.profile.trial_token = trial_token.key
    user.save()

    gmail_first_message(user_id,trial_token)

    return response


def user_info_get(user_id):
    user = User.objects.get(pk=user_id)
    if len(Token.objects.filter(user=user)) != 0 and not user.is_superuser:
        token_created = Token.objects.get(user=user).created
        token_time_remaining = timedelta(minutes=5)-(datetime.now(timezone.utc) - token_created)
        if token_time_remaining < timedelta(seconds=0):
            token_time_remaining = False
    else:
        token_time_remaining = False

    user_model_info = {
        'week_sub': user.profile.week_subscription,
        'month_sub': user.profile.month_subscription,
        'app_download': user.profile.app_download,
        'token_time_remaining': token_time_remaining
    }
    print(user_model_info)

    return user_model_info



def user_set_week_subscription(user_id):
    user = User.objects.get(pk=user_id)
    user.profile.week_subscription = True
    user.save()

def user_set_month_subscription(user_id):
    user = User.objects.get(pk=user_id)
    user.profile.month_subscription = True
    user.save()


def process_subscription(request):

    host = request.get_host()
    username = request.user.username
    user_id = request.user.id


    custom_list_week = [username,str(user_id),'week']
    packed_data_week = str.join('|',custom_list_week)
    custom_list_month = [username, str(user_id),'month']
    packed_data_month = str.join('|', custom_list_month)

    paypal_dict_week = {
        "cmd": "_xclick-subscriptions",
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        "a3": '0.1',  # monthly price
        "p3": 1,  # duration of each unit (depends on unit)
        "t3": 'W',  # duration unit ("M for Month")
        "src": "1",  # make payments recur
        "sra": "1",  # reattempt payment on payment error
        "no_note": "1",  # remove extra notes (optional)
        'item_name': 'Weekly subscription',
        'custom': packed_data_week,
        'currency_code': 'USD',
        'notify_url': 'http://{}{}'.format(host,
                                           reverse('paypal-ipn')),
        'return_url': 'http://{}{}'.format(host,
                                           reverse('payment_done')),
        'cancel_return': 'http://{}{}'.format(host,
                                              reverse('payment_canceled')),
    }

    form_week = PayPalPaymentsForm(initial=paypal_dict_week, button_type="subscribe")

    paypal_dict_month = {
        "cmd": "_xclick-subscriptions",
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        "a3": '0.1',  # monthly price
        "p3": 1,  # duration of each unit (depends on unit)
        "t3": 'M',  # duration unit ("M for Month")
        "src": "1",  # make payments recur
        "sra": "1",  # reattempt payment on payment error
        "no_note": "1",  # remove extra notes (optional)
        'item_name': 'Monthly subscription',
        'custom': packed_data_month,
        'currency_code': 'USD',
        'notify_url': 'http://{}{}'.format(host,
                                           reverse('paypal-ipn')),
        'return_url': 'http://{}{}'.format(host,
                                           reverse('payment_done')),
        'cancel_return': 'http://{}{}'.format(host,
                                              reverse('payment_canceled')),
    }

    form_month = PayPalPaymentsForm(initial=paypal_dict_month, button_type="subscribe")


    return [form_week,form_month]


@csrf_exempt
def payment_done(request):
    return render(request, 'process_payment.html')


@csrf_exempt
def payment_canceled(request):
    return render(request, 'ecommerce_app/payment_cancelled.html')

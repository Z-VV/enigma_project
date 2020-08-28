from django.shortcuts import render
from rest_framework import viewsets
from .serializers import HeroSerializer
from .models import Signals
from rest_framework.permissions import IsAuthenticated,IsAdminUser,IsAuthenticatedOrReadOnly
from rest_framework.decorators import api_view,permission_classes
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from datetime import datetime,timedelta,timezone

# Create your views here.

class HeroViewSet(viewsets.ModelViewSet):

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsAuthenticated]
        else:
            expire_token()
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    queryset = Signals.objects.all()
    serializer_class = HeroSerializer


def expire_token():
    for user in User.objects.all():

        if len(Token.objects.filter(user=user)) != 0 and not user.is_superuser:
            print(user.username)
            if not user.profile.trial_finished:
                token = Token.objects.get(user=user).key
                trial_token = user.profile.trial_token
                if token == trial_token:
                   token_created = Token.objects.get(user=user).created
                   if datetime.now(timezone.utc) -token_created > timedelta(minutes=5):
                        user.auth_token.delete()
                        user.profile.trial_finished = True
                        user.save()

            if user.profile.week_subscription:
                last_payment = user.profile.week_payment_date
                for x in range(5):
                    print(datetime.now(timezone.utc) - last_payment)
                if datetime.now(timezone.utc) - last_payment >= timedelta(minutes=5):
                    user.auth_token.delete()
                    user.profile.week_subscription = False
                    user.save()

            if user.profile.month_subscription:
                last_payment = user.profile.month_payment_date
                if datetime.now(timezone.utc) - last_payment >= timedelta(minutes=5):
                    user.auth_token.delete()
                    user.profile.month_subscription = False
                    user.save()














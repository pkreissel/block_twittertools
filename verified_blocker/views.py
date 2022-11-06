from django.shortcuts import render, redirect
from joblib import Parallel, delayed, parallel_backend
import os
import twitter as tw
import re
from django.http import JsonResponse, HttpResponse
import pandas as pd

APP_KEY = os.environ['APP_KEY']
APP_SECRET = os.environ['APP_SECRET']
verfied = pd.read_csv("verified_blocker/verified_twitter.txt")
# Create your views here.


def unfollow(request):
    if not "OAUTH_TOKEN" in request.session:
        print(request.get_full_path())
        request.session["REDIRECT"] = request.get_full_path()
        return redirect("/")
    api = tw.Api(consumer_key=APP_KEY,
                  consumer_secret=APP_SECRET,
                  access_token_key=request.session['OAUTH_TOKEN'],
                  access_token_secret=request.session['OAUTH_TOKEN_SECRET'],
                  tweet_mode='extended')
    friends = api.GetFriends()
    verified_friends = [friend.id for friend in friends if friend.verified]
    musk_friends = verified.loc[verified.isin(verfied_friends)]
    return render(request, 'block.html', {"users": musk_friends})

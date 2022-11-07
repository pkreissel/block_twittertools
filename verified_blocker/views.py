from django.shortcuts import render, redirect
from joblib import Parallel, delayed, parallel_backend
import os
import tweepy
import re
from django.http import JsonResponse, HttpResponse
import pandas as pd

APP_KEY = os.environ['APP_KEY']
APP_SECRET = os.environ['APP_SECRET']
verified = pd.read_csv("verified_blocker/verified_twitter.txt", names = ["i", "ids"])
verified_ids = verified.ids.astype(str)
print(verified_ids.values[:10])
# Create your views here.

def unfollow(request):
    if not "OAUTH_TOKEN" in request.session:
        print(request.get_full_path())
        request.session["REDIRECT"] = request.get_full_path()
        return redirect("/")
    api = tweepy.Client(
                    consumer_key=APP_KEY,
                    consumer_secret=APP_SECRET,
                    access_token=request.session['OAUTH_TOKEN'],
                    access_token_secret=request.session['OAUTH_TOKEN_SECRET'],
                 )
    friends = api.get_users_following(api.get_me(user_fields =["id"]).data.id, max_results = 1000, user_fields =["id","verified"], user_auth = True).data
    musk_friends = [friend for friend in friends if friend.verified and not str(friend.id) in verified_ids.values]
    verified_friends = [friend for friend in friends if friend.verified and str(friend.id) in verified_ids.values]
    print(verified_friends)
    return render(request, 'verified.html', {"musk_friends": musk_friends, "verified_friends": verified_friends})

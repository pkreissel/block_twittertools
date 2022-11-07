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
# Create your views here.

def verified(request):
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


def unfollow(request):
        if not "OAUTH_TOKEN" in request.session:
            return JsonResponse({'error': 'not_logged_in'})
        if request.method == "POST" and "OAUTH_TOKEN" in request.session:
            api = tweepy.Client(consumer_key=APP_KEY,
                         consumer_secret=APP_SECRET,
                         access_token=request.session['OAUTH_TOKEN'],
                         access_token_secret=request.session['OAUTH_TOKEN_SECRET'],
                        )
            if "profile_ids" in request.POST:
                accounts = request.POST.getlist("profile_ids")
                print(accounts)
                try:
                    with parallel_backend('threading', n_jobs=20):
                        Parallel()(delayed(unfollow_user)(api, block)
                                   for block in accounts)
                except Exception as e:
                    print(e)
                    return JsonResponse({'error': 'unknown error'})
            return HttpResponse("Success")
        return JsonResponse({'error': 'POST request not recognized'})

def unfollow_user(api, block):
    # print(screen_name)
    try:
        api.unfollow_user(id, user_auth=True)
        print("Success")
    except Exception as e:
        print(e)

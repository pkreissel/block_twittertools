from django.shortcuts import render, redirect
from joblib import Parallel, delayed, parallel_backend
import os
import tweepy
import re
from django.http import JsonResponse, HttpResponse

APP_KEY = os.environ['APP_KEY']
APP_SECRET = os.environ['APP_SECRET']

# Create your views here.


def blocklists(request):
    if not "OAUTH_TOKEN" in request.session:
        print(request.get_full_path())
        request.session["REDIRECT"] = request.get_full_path()
        return redirect("/")
    status_id = None
    users = None
    if request.method == "POST":
        print(request.POST)
        if "url" in request.POST:
            status_id = int(re.findall(
                "(?<=status\/)[^\/?]+", request.POST["url"])[0])
            print(status_id)
    if "tweet_id" in request.GET:
        status_id = request.GET["tweet_id"]
    if status_id:
        print("tweet_id")
        api = tweepy.Client(consumer_key=APP_KEY,
                      consumer_secret=APP_SECRET,
                      access_token=request.session['OAUTH_TOKEN'],
                      access_token_secret=request.session['OAUTH_TOKEN_SECRET']
                      )
        retweeters = api.get_retweeters(status_id, user_auth=True).data
        likers = api.get_liking_users(status_id, user_auth=True).data
        users = list(set(retweeters + likers))
    return render(request, 'block.html', {"users": users})


"""
Blocks mutliple users
:param request: the request
:return: success json message, otherwise an error in json response.
"""
def blockapi(request):
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
                    Parallel()(delayed(block_user)(api, block)
                               for block in accounts)
            except Exception as e:
                print(e)
                return JsonResponse({'error': 'unknown error'})
        return HttpResponse("Success")
    return JsonResponse({'error': 'POST request not recognized'})


def block_user(api, id=None):
    # print(screen_name)
    try:
        api.block(id, user_auth=True)
        print("Success")
    except Exception as e:
        print(e)

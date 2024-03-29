from django.shortcuts import render, redirect
from joblib import Parallel, delayed, parallel_backend
import os
import twitter as tw
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
    if request.method == "POST" and "OAUTH_TOKEN" in request.session:
        api = tw.Api(consumer_key=APP_KEY,
                     consumer_secret=APP_SECRET,
                     access_token_key=request.session['OAUTH_TOKEN'],
                     access_token_secret=request.session['OAUTH_TOKEN_SECRET'],
                     tweet_mode='extended')
        if "block" in request.POST:
            from . import blocklists
            try:
                with parallel_backend('threading', n_jobs=20):
                    Parallel()(delayed(block_user)(api, block, None)
                               for block in blocklists.block if not block in blocklists.error)
            except Exception as e:
                print(e)
        if "url" in request.POST:
            status_id = int(re.findall(
                "(?<=status\/)[^\/?]+", request.POST["url"])[0])
            retweeters = api.GetRetweeters(
                status_id, count=100, stringify_ids=True)
            # print(retweeters)
            try:
                with parallel_backend('threading', n_jobs=20):
                    Parallel()(delayed(block_user)(api, block, None)
                               for block in retweeters)
            except Exception as e:
                print(e)
    users = None
    if "users" in request.GET:
        users = request.GET["users"].split(",")
        if "tweet_id" in request.GET:
            print("tweet_id")
            api = tw.Api(consumer_key=APP_KEY,
                          consumer_secret=APP_SECRET,
                          access_token_key=request.session['OAUTH_TOKEN'],
                          access_token_secret=request.session['OAUTH_TOKEN_SECRET'],
                          tweet_mode='extended')
            retweets = api.GetRetweets(statusid = request.GET["tweet_id"])
            retweeters = [retweet.user.screen_name for retweet in retweets]
            users = list(set(retweeters + users))
            print(retweeters)
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
        api = tw.Api(consumer_key=APP_KEY,
                     consumer_secret=APP_SECRET,
                     access_token_key=request.session['OAUTH_TOKEN'],
                     access_token_secret=request.session['OAUTH_TOKEN_SECRET'],
                     tweet_mode='extended')
        if "profile_urls" in request.POST:
            accounts = request.POST.getlist("profile_urls")
            print(accounts)
            try:
                with parallel_backend('threading', n_jobs=20):
                    Parallel()(delayed(block_user)(api, None, block)
                               for block in accounts)
            except Exception as e:
                print(e)
                return JsonResponse({'error': 'unknown error'})
        return HttpResponse("Success")
    return JsonResponse({'error': 'POST request not recognized'})


def block_user(api, id=None, screen_name=None):
    # print(screen_name)
    try:
        api.CreateBlock(user_id=id, screen_name=screen_name)
        print("Success")
    except Exception as e:
        print(e)
        # pass
        # print(block)
        # print(e)

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
                    Parallel()(delayed(block_user)(block, api) for block in blocklists.block if not block in blocklists.error)
            except Exception as e:
                print(e)
        if "url" in request.POST:
            status_id = int(re.findall("(?<=status\/)[^\/?]+", request.POST["url"])[0])
            retweeters = api.GetRetweeters(status_id, count=100, stringify_ids=True)
            #print(retweeters)
            try:
                with parallel_backend('threading', n_jobs=20):
                    Parallel()(delayed(block_user)(block, api) for block in retweeters)
            except Exception as e:
                print(e)
    users = None
    if "users" in request.GET:
        users = request.GET["users"].split(",")
    return render(request, 'block.html', {"users": users})

"""
Blocks mutliple users
:param request: the request
:return: success json message, otherwise an error in json response.
"""
def blockapi(request):
    if not "OAUTH_TOKEN" in request.session:
        return JsonResponse({'error':'not_logged_in'})
    if request.method == "POST" and "OAUTH_TOKEN" in request.session:
        api = tw.Api(consumer_key=APP_KEY,
                      consumer_secret=APP_SECRET,
                      access_token_key=request.session['OAUTH_TOKEN'],
                      access_token_secret=request.session['OAUTH_TOKEN_SECRET'],
                      tweet_mode='extended')
        if "profile_urls" in request.POST:
            accounts = request.POST.getlist("profile_urls")
            try:
                with parallel_backend('threading', n_jobs=20):
                    Parallel()(delayed(block_user)(block, api) for block in accounts)
            except Exception as e:
                return JsonResponse({'error':'unknown error'})
                print(e)
        return HttpResponse("Success")
    return JsonResponse({'error':'POST request not recognized'})

def block_user(block, api):
    try:
        api.CreateBlock(user_id=block)
        print("Success")
    except Exception as e:
        print(e)
        #pass
        #print(block)
        #print(e)

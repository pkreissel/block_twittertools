from django.shortcuts import render, redirect
from django.http import HttpResponse
import re
import os
from django.conf import settings
import tweepy


APP_KEY = os.environ['APP_KEY']
APP_SECRET = os.environ['APP_SECRET']
CALLBACK = os.environ['ROOT_PROD'] + "/callback"
if settings.DEBUG:
    CALLBACK = os.environ['ROOT_TEST'] + "/callback"

print(CALLBACK)

def index(request):
    oauth1_user_handler = tweepy.OAuth1UserHandler(
        APP_KEY, APP_SECRET,
        callback=CALLBACK
    )
    login_url = oauth1_user_handler.get_authorization_url()
    request.session['request_token'] = oauth1_user_handler.request_token["oauth_token"]
    request.session['request_secret'] = oauth1_user_handler.request_token["oauth_token_secret"]
    return render(request, 'index.html', {
        "login_url": login_url,
        })

def callback(request):
    oauth1_user_handler = tweepy.OAuth1UserHandler(
        APP_KEY, APP_SECRET,
        callback=CALLBACK
    )
    oauth1_user_handler.request_token = {
        "oauth_token": request.session['request_token'],
        "oauth_token_secret": request.session['request_secret']
    }

    access_token, access_token_secret = oauth1_user_handler.get_access_token(
        request.GET['oauth_verifier']
    )
    request.session['OAUTH_TOKEN'] = access_token
    request.session['OAUTH_TOKEN_SECRET'] = access_token_secret

    if "REDIRECT" in request.session:
        redir_url = request.session["REDIRECT"]
        request.session.pop("REDIRECT", None)
        return redirect(redir_url)
    return redirect("/")

def api(request):
    return HttpResponse("Hello world")

def logout(request):
    request.session.pop("OAUTH_TOKEN", None)
    request.session.pop("OAUTH_TOKEN_SECRET", None)
    return redirect("/")

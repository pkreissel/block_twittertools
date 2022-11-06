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

oauth1_user_handler = tweepy.OAuth1UserHandler(
    APP_KEY, APP_SECRET,
    callback=CALLBACK
)

def index(request):
    if not "OAUTH_TOKEN" in request.session:


    return render(request, 'index.html', {
        "login_url": oauth1_user_handler.get_authorization_url(),
        })

def callback(request):
    try:
        access_token, access_token_secret = oauth1_user_handler.get_access_token(
            request.GET['oauth_verifier']
        )
        request.session['OAUTH_TOKEN'] = access_token
        request.session['OAUTH_TOKEN_SECRET'] = access_token_secret
    except Exception as e:
        print("error occured")
        print(e)
        return HttpResponse(e)
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

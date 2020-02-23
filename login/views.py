from django.shortcuts import render, redirect
from django.http import HttpResponse
from twython import Twython
import re
import os
from django.conf import settings


APP_KEY = os.environ['APP_KEY']
APP_SECRET = os.environ['APP_SECRET']
CALLBACK = 'https://ichbinhier-twittertools.herokuapp.com/callback'
if settings.DEBUG:
    CALLBACK = "http://127.0.0.1:8000/callback"

def index(request):
    if not "OAUTH_TOKEN" in request.session:
        twitter = Twython(APP_KEY, APP_SECRET)
        auth = twitter.get_authentication_tokens(callback_url=CALLBACK)
        request.session["Login_TOKEN"] = auth['oauth_token']
        request.session["Login_TOKEN_Secret"] = auth['oauth_token_secret']
        request.session["auth_url"] = auth['auth_url']

    return render(request, 'index.html', {
        "login_url": request.session["auth_url"],
        })



def callback(request):
    try:
        oauth_verifier = request.GET['oauth_verifier']
        twitter = Twython(APP_KEY,APP_SECRET,request.session["Login_TOKEN"],request.session["Login_TOKEN_Secret"])
        final_step = twitter.get_authorized_tokens(oauth_verifier)
        request.session['OAUTH_TOKEN'] = final_step['oauth_token']
        request.session['OAUTH_TOKEN_SECRET'] = final_step['oauth_token_secret']
    except Exception as e:
        print(e)
    if "REDIRECT" in request.session:
        redir_url = request.session["REDIRECT"]
        request.session.pop("REDIRECT", None)
        return redirect(redir_url)
    return redirect("/")

def api(request):
    return HttpResponse("Hello world")

def logout(request):
    del(request.session["OAUTH_TOKEN"])
    return redirect("/")

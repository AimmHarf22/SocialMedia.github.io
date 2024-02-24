from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from media.models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
import datetime


# Create your views here.

def index(request):
    if not request.user.is_authenticated:
        return render(request, "media/login.html")
    return render(request, "media/index.html")


def register(request):
    # Check For Request method
    if request.method == "POST":
        # Post Data
        first_name = request.POST["firstName"]
        last_name = request.POST["lastName"]
        email = request.POST["email"]
        username = request.POST["username"]
        password = request.POST["password"]
        password2 = request.POST["password2"]

        # VALIDATION

        # Check for empty boxes
        if (
            len(first_name) == 0
            or len(last_name) == 0
            or len(email) == 0
            or len(username) == 0
            or len(password) == 0
            or len(password2) == 0
        ):
            return render(
                request, "register.html", {"message": "All Fields Must Not Be blank"}
            )

            # Check if the passwords match
        if password != password2:
            return render(
                request, "media/register.html", {"message": "Password Does Not Match"}
            )

            # Check if email is valid
        if not "@" in email:
            return render(request, "media/register.html", {"message": "Invalid Email"})

            # Check if password is strong
        if not len(password) > 4:
            return render(
                request, "media/register.html", {"message": "Password is weak"}
            )

            # Check if username exists
        try:
            check = User.objects.get(username=username)
            if len(check.username) > 0:
                return render(
                    request,
                    "media/register.html",
                    {"message": "Username already exists"},
                )
            else:
                pass
        except ObjectDoesNotExist as e:
            pass

        # ADD DATA TO DATABASE
        
        user = User.objects.create_user(username=username,password=password,first_name=first_name,last_name=last_name,email=email,)
        user.save()
        return HttpResponseRedirect(reverse("login"))

    else:
        return render(request, "media/register.html")


def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "media/login.html", {"message":"Invalid Username or Password"})
    return render(request, "media/login.html")

def logout_user(request):

    logout(request)
    return HttpResponseRedirect(reverse("index"))

def new_posts(request):
    if request.method == 'POST':
        post = request.POST['post']

        new_post=Posts(first_name=request.user.first_name, last_name=request.user.last_name, username=request.user.username, post=post, date=datetime.datetime.now())

        new_post.save()

        return HttpResponseRedirect(reverse("index"))
    
    return render(request, "media/newpost.html")
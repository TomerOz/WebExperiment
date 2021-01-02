from django.shortcuts import render, redirect, reverse

from django.contrib.auth import login, logout, authenticate
from .forms import RegisterForm
import ipdb

#targetPageToURL = {"SGS1" : "profilePresntaion/PhaseDecision", None : 'home/home'} # for simple "redirect"
targetPageToURL = {"SGS1" : "profilePresntaion:PhaseDecision", None : 'home:home'} # for "reverse" --> totally new path


def logout_user(request):
    logout(request)
    return redirect(reverse('home:home'))

def signup(request, targetPage=None):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=raw_password)
            login(request, user)
            #return redirect(targetPageToURL[targetPage])
            return redirect(reverse(targetPageToURL[targetPage]))
    else:
        form = RegisterForm()

    return render(request, 'Register/signup.html', {'form': form, "targetURLAfterLogin": targetPage})

def signin(request, targetPage=None):
    if request.method == 'POST': # User tries to login
        logout(request)
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(email=email, password=password)
        form_feedback = {}
        if user != None: # Successful login
            login(request, user)
            #request.session.set_expiry(60*60) # Controls time in seconds for sesssion expiery
            return redirect(reverse(targetPageToURL[targetPage]))

        else: # Errors
            form_feedback["errors"] = "Invalid Details"
            return render(request, 'Register/signin.html', form_feedback)

    else: # User is about to login
        return render(request, 'Register/signin.html', {"targetURLAfterLogin": targetPage})

from django.shortcuts import render, redirect, reverse

from django.contrib.auth import login, logout, authenticate
from .forms import RegisterForm
from django.contrib.auth.forms import UserCreationForm
import ipdb

#targetPageToURL = {"SGS1" : "profilePresntaion/PhaseDecision", None : 'home/home'} # for simple "redirect"
targetPageToURL = {"SGS1" : "profilePresntaion:PhaseDecision", "ipa_1_2": "ipa_1_2:PhaseDecision", 'Home' : 'home:home'} # for "reverse" --> totally new path


def logout_user(request):
    logout(request)
    return redirect(reverse('home:home'))

def signup(request, targetPage="Home"):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if not request.POST["subject_set"] in ["A","B","C"]:
            return render(request, 'Register/signup.html', {'errors': "Must choose a value", "targetURLAfterLogin": targetPage})
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            user.usertosubject.subject_num = request.POST["subject_num"]
            user.usertosubject.features_set = request.POST["subject_set"]
            user.usertosubject.education = request.POST["education"]
            user.usertosubject.age = request.POST["age"]
            user.usertosubject.gender = request.POST["gender"]
            user.usertosubject.runningLocation = request.POST["runningLocation"]
            user.save()
            if request.POST["flow"] == "continue":
                return redirect("/signup/" + username)
            else:
                login(request, user)
            return redirect(targetPageToURL[targetPage])
        else:
            return render(request, 'Register/signup.html', {'form': form, "targetURLAfterLogin": targetPage, 'registrationErrors': "Invalid deatils - not registered" })
    else:
        form = RegisterForm()

    return render(request, 'Register/signup.html', {'form': form, "targetURLAfterLogin": targetPage})

def signin(request, targetPage="Home"):
    if request.method == 'POST': # User tries to login
        logout(request)
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
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


# old sign up and sign in - when user names where emails

# def signup(request, targetPage=None):
#     if request.method == 'POST':
#         form = RegisterForm(request.POST)
#         if form.is_valid():
#             form.save()
#             email = form.cleaned_data.get('email')
#             raw_password = form.cleaned_data.get('password1')
#             user = authenticate(email=email, password=raw_password)
#             login(request, user)
#             #return redirect(targetPageToURL[targetPage])
#             return redirect(reverse(targetPageToURL[targetPage]))
#     else:
#         form = RegisterForm()
#
#     return render(request, 'Register/signup.html', {'form': form, "targetURLAfterLogin": targetPage})

# def signin(request, targetPage=None):
#     if request.method == 'POST': # User tries to login
#         logout(request)
#         email = request.POST["email"]
#         password = request.POST["password"]
#         user = authenticate(email=email, password=password)
#         form_feedback = {}
#         if user != None: # Successful login
#             login(request, user)
#             #request.session.set_expiry(60*60) # Controls time in seconds for sesssion expiery
#             return redirect(reverse(targetPageToURL[targetPage]))
#
#         else: # Errors
#             form_feedback["errors"] = "Invalid Details"
#             return render(request, 'Register/signin.html', form_feedback)
#
#     else: # User is about to login
#         return render(request, 'Register/signin.html', {"targetURLAfterLogin": targetPage})

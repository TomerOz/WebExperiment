from django.shortcuts import render, redirect, reverse

from django.contrib.auth import login, logout, authenticate
from .forms import RegisterForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

import ipdb

#targetPageToURL = {"SGS1" : "profilePresntaion/PhaseDecision", None : 'home/home'} # for simple "redirect"
targetPageToURL = {"ipa_2" : "ipa_2:PhaseDecision", "ipa_1_2": "ipa_1_2:PhaseDecision", 'Home' : 'home:home'} # for "reverse" --> totally new path


def process_sign_ups(post_data):
    questions_answers = {
        "subject_set": ["A","B","C"],
        "runningLocation": ["Lab", "Home"],
        "assignesExperiment": ["IPA_1.2","IPA_2"],
        "gender": ["female", "male"],
        }

    errors = {}
    filled_ok = {}
    for k,v in questions_answers.items():
        if not post_data[k] in v:
            errors[k+"_errors"] = "Must choose a value"
        else:
            filled_ok["selected"+post_data[k]] = "selected"
    return (errors, filled_ok)

def logout_user(request):
    logout(request)
    return redirect(reverse('home:home'))

def signup(request, targetPage="Home"):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        errors, filled_ok = process_sign_ups(request.POST)
        if len(errors) > 0:
            context = {"targetURLAfterLogin": targetPage, "selectedUserName":  request.POST["username"], "selectedSubject_num": request.POST["subject_num"]}
            context.update(errors)
            context.update(filled_ok)
            return render(request, 'Register/signup.html', context)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            user.first_name = request.POST["assignesExperiment"]
            user.save()
            if request.POST["assignesExperiment"] == "IPA_1.2":
                from ipa_1_2.models import create_user_subject
                create_user_subject(User, user, True)
                user.usertosubject.save()
                user.usertosubject.subject_num = request.POST["subject_num"]
                user.usertosubject.features_set = request.POST["subject_set"]
                user.usertosubject.runningLocation = request.POST["runningLocation"]
                user.usertosubject.gender = request.POST["gender"]
                user.usertosubject.save()

            elif request.POST["assignesExperiment"] == "IPA_2":
                from ipa_2.models import create_user_subject
                create_user_subject(User, user, True)
                user.usertosubject.save()
                user.usertosubjectipa2.subject_num = request.POST["subject_num"]
                user.usertosubjectipa2.features_set = request.POST["subject_set"]
                user.usertosubjectipa2.runningLocation = request.POST["runningLocation"]
                user.usertosubjectipa2.gender = request.POST["gender"]
                user.usertosubject.save()
            # user.usertosubject.education = request.POST["education"]
            # user.usertosubject.age = request.POST["age"]
            if request.POST["flow"] == "continue":
                return redirect("/signup/" + username)
            else:
                login(request, user)
            return redirect(targetPageToURL[targetPage])
        else:
            context = {'form': form, "targetURLAfterLogin": targetPage, 'registrationErrors': "Invalid deatils - not registered" }
            context.update({"selectedUserName":  request.POST["username"], "selectedSubject_num": request.POST["subject_num"]})
            context.update(errors)
            context.update(filled_ok)

            return render(request, 'Register/signup.html', context)
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

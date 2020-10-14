from django.shortcuts import render, redirect

from django.contrib.auth import login, logout, authenticate
from .forms import RegisterForm
import ipdb

def signup(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=raw_password)
            login(request, user)
            # return redirect('home')
            return render(request, 'profilePresntaion/index.html')
    else:
        form = RegisterForm()

    return render(request, 'Register/signup.html', {'form': form})
#sdfg45345fgsdf4

def signin(request):
    if request.method == 'POST':
        logout(request)
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(email=email, password=password)
        form_feedback = {}
        if user != None:
            login(request, user)
        else:
            form_feedback["errors"] = "Invalid Details"
        return render(request, 'Register/signin.html', form_feedback)
    else:
        return render(request, 'Register/signin.html' )

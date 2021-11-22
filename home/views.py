from django.shortcuts import render, redirect, reverse
from django.shortcuts import redirect
from django.contrib.auth import logout

targetPageToURL = {"SGS1" : "profilePresntaion:PhaseDecision", "ipa_1_2": "ipa_1_2:PhaseDecision", None : 'home:home'} # for "reverse" --> totally new path

# Create your views here.
def home_page(request):
    if request.method == "GET":
        return render(request, 'home/home.html')

    elif request.method == "POST": # TODO: Now this logic reilies on only one form (one experiment option) in home page, later I'll have to know which form is it
        target_experiment = request.POST["form_phase"] # Something like "SGS1"
        if request.user.is_authenticated:
            if target_experiment == "logout":
                logout(request)
                return redirect(reverse(targetPageToURL[None]))
            else:
                return redirect(reverse(targetPageToURL[target_experiment]))
        else:
            import os
            x = os.getcwd()
            return redirect('signup/' + target_experiment, {"x":x})

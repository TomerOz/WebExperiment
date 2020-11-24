from django.shortcuts import render, redirect, reverse
from django.shortcuts import redirect

targetPageToURL = {"SGS1" : "profilePresntaion:PhaseDecision", None : 'home:home'} # for "reverse" --> totally new path

# Create your views here.
def home_page(request):
    if request.method == "GET":
        return render(request, 'home/home.html',)

    elif request.method == "POST": # TODO: Now this logic reilies on only one form (one experiment option) in home page, later I'll have to know which form is it
        target_experiment = request.POST["form_phase"] # Something like "SGS1"
        if request.user.is_authenticated:
            return redirect(reverse(targetPageToURL[target_experiment]))
        else:
            return redirect('signin/' + target_experiment)
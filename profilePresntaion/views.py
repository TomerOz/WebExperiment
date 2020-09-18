from django.shortcuts import render, get_object_or_404
from .models import Profile

# Create your views here.
def index(request):
    return render(request, 'profilePresntaion/Index.html')
def present_profile(request, profile_pk):
    profile = get_object_or_404(Profile, pk=profile_pk)
    return render(request, 'profilePresntaion/profile.html', {'profile': profile})

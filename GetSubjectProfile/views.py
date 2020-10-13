from django.shortcuts import render

# Create your views here.
def home_page():
    return render(request, 'GetSubjectProfile/HomePage.html')

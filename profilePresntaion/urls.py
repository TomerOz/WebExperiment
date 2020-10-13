from django.urls import path

from . import views

app_name = 'profilePresntaion'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:profile_pk>/', views.present_profile, name='present_profile'),
]

from django.urls import path

from . import views

app_name = 'profilePresntaion'
urlpatterns = [
    #path('', views.index, name='index'),
    path('', views.get_phase_page, name='PhaseDecision'), # A general requests handler that dicides on subject's phase
    path('<int:profile_pk>/', views.get_page_present_profile, name='present_profile'),
    path('getSubjectProfile/', views.get_page_get_subject_profile, name='getSubjectProfile'),
]

from django.urls import path

from . import views

app_name = 'ipa_1_2'
urlpatterns = [
    path('', views.get_phase_page, name='PhaseDecision'), # A general requests handler that dicides on subject's phase
    path('<int:profile_pk>/', views.get_page_present_profile, name='present_profile'),
    path('getSubjectProfile/', views.get_page_get_subject_profile, name='getSubjectProfile'),
]
 # 13.07.21 -> needs to be change for being called from the correct page at home, but maybe it still works

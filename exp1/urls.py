"""exp1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from Register import views as register_views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', include('home.urls')),
    path('signup/', register_views.signup, name='signup'),
    path('signin/', register_views.signin, name='signin'),
    path('signin/<str:targetPage>', register_views.signin, name='signin'), # singin with argeument
    path('signup/<str:targetPage>', register_views.signup, name='signup'), # signup with argeument
    path('profilePresntaion/', include('profilePresntaion.urls')),
    path('ipa_1_2/', include('ipa_1_2.urls')),
    #path('GetSubjectProfile/', include('GetSubjectProfile.urls')),
    path('admin/', admin.site.urls),
    path('logout/', register_views.logout_user, name="logout"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

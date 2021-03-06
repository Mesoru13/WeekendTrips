"""WeekendTrips URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path
from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    url('results/', views.results, name='results'),
    url('get_task/', views.get_task, name='get_task'),
    url('commit_task/', views.commit_task, name='commit_task'),
    url('get_cities/', views.get_cities, name='get_cities'),
    url('get_task_result/', views.get_task_result, name='get_task_result'),
    url('', views.home, name='home')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

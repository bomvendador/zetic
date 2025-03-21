"""reports URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from api import views

from django.conf.urls import handler400, handler403, handler404, handler500


handler404 = 'panel.views.page_not_found'
# handler400 = 'reports.panel_views.page_not_found'


urlpatterns = [
    path('', views.home, name='home'),
    # path('json_request/', views.json_request, name='json_request'),
    path('admin/', admin.site.urls),
    path('pdf/', include('pdf.urls'), name='pdf'),
    path('api/', include('api.urls'), name='api'),
    path('login/', include('login.urls'), name='login'),
    path('panel/', include('panel.urls'), name='panel'),
    path('questionnaire/', include('questionnaire.urls'), name='questionnaire'),
]

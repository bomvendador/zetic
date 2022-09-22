from django.urls import path
from api import views

urlpatterns = [
    path('', views.server_response, name="server_response"),
    path('single-report/v1', views.json_request, name="json"),
]
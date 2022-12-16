from django.urls import path
from api import views
from . import outcoming

urlpatterns = [
    path('', views.server_response, name="server_response"),
    path('single-report/v1', views.json_request, name="json"),
    path('group-report/v1', views.json_request, name="json"),
    path('get_code_for_invitation', outcoming.get_code_for_invitation, name="get_code_for_invitation"),

]
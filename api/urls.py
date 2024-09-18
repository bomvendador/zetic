from django.urls import path
from api import views
from . import outcoming
from . import incoming


urlpatterns = [
    path('', views.server_response, name="server_response"),
    # path('single-report/v1', incoming.data_for_report, name="json"),
    # path('group-report/v1', views.json_request, name="json"),
    # path('get_code_for_invitation', outcoming.get_code_for_invitation, name="get_code_for_invitation"),
    path('participant_started', incoming.participant_started, name="participant_started"),
    path('questions_answered_qnt', incoming.questions_answered_qnt, name="questions_answered_qnt"),
    path('companies_employees', incoming.companies_employees, name="companies_employees"),

]
from pdf.models import Employee, Company, EmployeePosition, EmployeeRole, Industry, Study
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseServerError, JsonResponse

import json


@login_required(redirect_field_name=None, login_url='/login/')
def get_code_for_invitation(request, json_request):

    return 'josipfjsdof'


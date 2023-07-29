from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .views import info_common


@login_required(redirect_field_name=None, login_url="/login/")
def individual_report_file_index(request):
    context = info_common(request)
    context.update({})

    return render(request, "panel_add_individual_report.html", context)

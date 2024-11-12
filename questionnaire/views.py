from pdf.models import CommonBooleanSettings

from django.shortcuts import render
import time

# Create your views here.


def questionnaire_context():
    tech_works_mode = CommonBooleanSettings.objects.get(name='Технические работы').value

    context = {
        'timestamp': time.time(),
        'tech_works': tech_works_mode,
    }
    return context

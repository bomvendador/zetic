from django.shortcuts import render
import time

# Create your views here.


def questionnaire_context():
    context = {
        'timestamp': time.time()
    }
    return context

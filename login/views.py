from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .models import UserProfile
from pdf.models import Employee
import json
# Create your views here.


def home(request):
    context = {}
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        user_login = json_data['login']
        user_password = json_data['password']
        user = authenticate(username=user_login, password=user_password)
        if user is not None:
            if user.is_active:
                user_profile = UserProfile.objects.get(user=user)
                if user_profile.role.name == 'Админ заказчика':
                    employee = Employee.objects.get(user=user)
                    if not employee.company_admin_active:
                        return HttpResponse(json.dumps({
                            'response': 'error',
                            'text': 'Ваша учетная запись деактивирована'
                        }))
                    else:
                        login(request, user)
                        return HttpResponse(user.id)
                else:
                    login(request, user)
                    return HttpResponse(user.id)
        else:
            return HttpResponse(json.dumps({
                'response': 'error',
                'text': 'Логин и/или пароль указаны не верно'
            }))

    return render(request, 'login.html', context)





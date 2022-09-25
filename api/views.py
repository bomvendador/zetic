from django.http import HttpResponseServerError, HttpResponse
import json
from pdf.views import pdf_generator
from django.shortcuts import render
import ast
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

# Create your views here.


def server_response(request):
    return HttpResponse(status=200)


@method_decorator(csrf_exempt, name='dispatch')
def json_request(request):
    if request.method == 'POST':
        try:
            print('POST', request.POST)
            print('BODY', request.body)
            rp = json.loads(request.body.decode('utf-8'))
            print('JSON', rp['frames'])

            # print(request.POST)
            # pr = ast.literal_eval(request.body)
            # print(pr)
            #
            # pr2 = json.loads(request.body.decode('utf-8'))
            # print(pr2)

            request_json = json.loads(str(ast.literal_eval(str(dict(request.POST)))))

            kew = '{   "code": "eiZoo7ie5vaighee7aiZei7d",   "participant_info": {     "name": "Дваркович Владимир",     "sex": "женский",     "birth_year": "1987",     "email": "dvarkovich@email.com"   },   "lie_points": 3,   "appraisal_data": [     {       "section": "Копинги",       "point": [         {"category":"Самообладание", "points": 7},         {"category":"Контроль над ситуацией", "points":7},         {"category":"Позитивная самомотивация", "points": 7},         {"category":"Снижение значения стрессовой ситуации", "points": 10},         {"category":"Самоутверждение", "points": 5},         {"category":"Отвлечение", "points": 7},         {"category":"Бегство от стрессовой ситуации", "points": 5},         {"category":"Антиципирующее избегание", "points": 5},         {"category":"Замещение", "points": 5},         {"category":"Поиск социальной поддержки", "points": 4},         {"category":"Жалость к себе", "points": 7},         {"category":"Социальная замкнутость", "points": 3},         {"category":"Самообвинение", "points": 5},         {"category": "Заезженная пластинка", "points": 4},         {"category":"Самооправдание", "points": 6},         {"category":"Агрессия", "points": 4}       ]     },     {       "section": "Выгорание Бойко",       "point": [         {"category":"Напряжение_Переживание", "points": 5},         {"category":"Напряжение_Неудовлетворенность собой", "points":4},         {"category":"Напряжение_Загнанность в клетку", "points": 2},         {"category":"Напряжение_Тревога", "points": 7},         {"category":"Сопротивление_Избирательное реагирование", "points": 5},         {"category":"Сопротивление_Эмоциональная защита", "points": 1},         {"category":"Сопротивление_Экономия эмоций", "points": 7},         {"category":"Сопротивление_Эмпатическая усталость", "points": 8},         {"category":"Истощение_Эмоциональная опустошенность", "points": 2},         {"category":"Истощение_Эмоциональная отстраненность", "points": 2},         {"category":"Истощение_Личностная отстраненность", "points": 9},         {"category":"Истощение_Психосоматика", "points":8}       ]     },     {       "section": "Ценности",       "point": [         {"category":"Причастность", "points": 10},         {"category":"Традицонализм", "points":7},         {"category":"Жажда впечатлений", "points": 6},         {"category":"Эстетичность", "points": 9},         {"category":"Гедонизм", "points": 9},         {"category":"Признание", "points": 10},         {"category":"Достижения", "points": 6},         {"category":"Коммерческий подход", "points": 5},         {"category":"Безопасность", "points": 7},         {"category":"Интеллект", "points": 4}       ]     },     {       "section": "Кеттелл",       "point": [         {"category":"Шкала C", "points": 10},         {"category":"Шкала O", "points":7},         {"category":"Шкала Q4", "points": 6},         {"category":"Шкала F", "points": 9},         {"category":"Шкала N", "points": 9},         {"category":"Шкала I", "points": 10},         {"category":"Шкала A", "points": 6},         {"category":"Шкала M", "points": 5},         {"category":"Шкала Q2", "points": 7},         {"category":"Шкала G", "points": 4},         {"category":"Шкала Q3", "points": 4},         {"category":"Шкала Q1", "points": 4},         {"category":"Шкала L", "points": 4},         {"category":"Шкала H", "points": 4},         {"category":"Шкала E", "points": 4}       ]     }   ] }'
            # request_json = json.loads(kew)
            print(request_json)
        except KeyError:
            HttpResponseServerError('JSON request error')
    else:
        file = 'media/json/single-report-example.json'
        with open(file, encoding="utf8") as f:
            request_json = json.load(f)

    return pdf_generator(request_json)


def home(request):
    context = {}
    return render(request, 'report_v1.html', context)

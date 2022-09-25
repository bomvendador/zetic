import logging
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reports.settings')
from rest_framework.test import APIRequestFactory
from django.test import Client

# logging.basicConfig(filename='test.log', level=logging.DEBUG)

factory = APIRequestFactory()
json = {
          "code": "eiZoo7ie5vaighee7aiZei7d",
          "participant_info": {
            "name": "Дваркович Владимир",
            "sex": "женский",
            "birth_year": "1987",
            "email": "dvarkovich@email.com"
          },
          "lie_points": 3,
          "appraisal_data": [
            {
              "section": "Копинги",
              "point": [
                {"category":"Самообладание", "points": 7},
                {"category":"Контроль над ситуацией", "points":7},
                {"category":"Позитивная самомотивация", "points": 7},
                {"category":"Снижение значения стрессовой ситуации", "points": 10},
                {"category":"Самоутверждение", "points": 5},
                {"category":"Отвлечение", "points": 7},
                {"category":"Бегство от стрессовой ситуации", "points": 5},
                {"category":"Антиципирующее избегание", "points": 5},
                {"category":"Замещение", "points": 5},
                {"category":"Поиск социальной поддержки", "points": 4},
                {"category":"Жалость к себе", "points": 7},
                {"category":"Социальная замкнутость", "points": 3},
                {"category":"Самообвинение", "points": 5},
                {"category": "Заезженная пластинка", "points": 4},
                {"category":"Самооправдание", "points": 6},
                {"category":"Агрессия", "points": 4}
              ]
            },
            {
              "section": "Выгорание Бойко",
              "point": [
                {"category":"Напряжение_Переживание", "points": 5},
                {"category":"Напряжение_Неудовлетворенность собой", "points":4},
                {"category":"Напряжение_Загнанность в клетку", "points": 2},
                {"category":"Напряжение_Тревога", "points": 7},
                {"category":"Сопротивление_Избирательное реагирование", "points": 5},
                {"category":"Сопротивление_Эмоциональная защита", "points": 1},
                {"category":"Сопротивление_Экономия эмоций", "points": 7},
                {"category":"Сопротивление_Эмпатическая усталость", "points": 8},
                {"category":"Истощение_Эмоциональная опустошенность", "points": 2},
                {"category":"Истощение_Эмоциональная отстраненность", "points": 2},
                {"category":"Истощение_Личностная отстраненность", "points": 9},
                {"category":"Истощение_Психосоматика", "points":8}
              ]
            },
            {
              "section": "Ценности",
              "point": [
                {"category":"Причастность", "points": 10},
                {"category":"Традицонализм", "points":7},
                {"category":"Жажда впечатлений", "points": 6},
                {"category":"Эстетичность", "points": 9},
                {"category":"Гедонизм", "points": 9},
                {"category":"Признание", "points": 10},
                {"category":"Достижения", "points": 6},
                {"category":"Коммерческий подход", "points": 5},
                {"category":"Безопасность", "points": 7},
                {"category":"Интеллект", "points": 4}
              ]
            },
            {
              "section": "Кеттелл",
              "point": [
                {"category":"Шкала C", "points": 10},
                {"category":"Шкала O", "points":7},
                {"category":"Шкала Q4", "points": 6},
                {"category":"Шкала F", "points": 9},
                {"category":"Шкала N", "points": 9},
                {"category":"Шкала I", "points": 10},
                {"category":"Шкала A", "points": 6},
                {"category":"Шкала M", "points": 5},
                {"category":"Шкала Q2", "points": 7},
                {"category":"Шкала G", "points": 4},
                {"category":"Шкала Q3", "points": 4},
                {"category":"Шкала Q1", "points": 4},
                {"category":"Шкала L", "points": 4},
                {"category":"Шкала H", "points": 4},
                {"category":"Шкала E", "points": 4}
              ]
            }
          ]
        }

# logging.info(json)
# requestAPI = factory.post('/pdf/fpdf', json, format='json')
c = Client()
response = c.post('/pdf/fpdf', json)
print(response.status_code)




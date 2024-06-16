from pdf.models import EmployeePosition, EmployeeRole, Industry, User, Participant, EmployeeGender

import rstr

squares_data = [
    {
        'code': '1_1',
        'square_name': 'ИНТЕГРАТОРЫ',
        'square_role_name': 'Магнит'
    },
    {
        'code': '1_2',
        'square_name': 'ИНТЕГРАТОРЫ',
        'square_role_name': 'Фасилитатор'
    },
    {
        'code': '1_3',
        'square_name': 'ИНТЕГРАТОРЫ',
        'square_role_name': 'Переговорщик'
    },
    {
        'code': '1_4',
        'square_name': 'ИНТЕГРАТОРЫ',
        'square_role_name': 'Коннектор'
    },
    {
        'code': '2_1',
        'square_name': 'ПРЕДПРИНИМАТЕЛИ',
        'square_role_name': 'Визионер'
    },
    {
        'code': '2_2',
        'square_name': 'ПРЕДПРИНИМАТЕЛИ',
        'square_role_name': 'Авантюрист'
    },
    {
        'code': '2_3',
        'square_name': 'ПРЕДПРИНИМАТЕЛИ',
        'square_role_name': 'Искатель ресурсов'
    },
    {
        'code': '2_4',
        'square_name': 'ПРЕДПРИНИМАТЕЛИ',
        'square_role_name': 'Изобретатель'
    },
    {
        'code': '3_1',
        'square_name': 'АДМИНИСТРАТОРЫ',
        'square_role_name': 'Хранитель'
    },
    {
        'code': '3_2',
        'square_name': 'АДМИНИСТРАТОРЫ',
        'square_role_name': 'Вдохновитель'
    },
    {
        'code': '3_3',
        'square_name': 'АДМИНИСТРАТОРЫ',
        'square_role_name': 'Контролер'
    },
    {
        'code': '3_4',
        'square_name': 'АДМИНИСТРАТОРЫ',
        'square_role_name': 'Благородный служитель'
    },
    {
        'code': '4_1',
        'square_name': 'ПРОИЗВОДИТЕЛИ',
        'square_role_name': 'Организатор'
    },
    {
        'code': '4_2',
        'square_name': 'ПРОИЗВОДИТЕЛИ',
        'square_role_name': 'Любитель улучшений'
    },
    {
        'code': '4_3',
        'square_name': 'ПРОИЗВОДИТЕЛИ',
        'square_role_name': 'Реализатор'
    },
    {
        'code': '4_4',
        'square_name': 'ПРОИЗВОДИТЕЛИ',
        'square_role_name': 'Решатель проблем'
    },
]


def generate_code(symbol_qnt):
    code = ''
    for i in range(symbol_qnt):
        code = code + rstr.xeger(r'([A-Z]|[a-z]|[1-9])')
    return code


def update_attributes(request, response):
    sex = response['sex']
    positions = response['position']
    industries = response['industry']
    roles = response['role']
    for item in roles:
        item_inst_qnt = EmployeeRole.objects.filter(public_code=item['id']).count()
        if item_inst_qnt == 0:
            inst = EmployeeRole()
            inst.created_by = request.user
            inst.public_code = item['id']
        else:
            inst = EmployeeRole.objects.get(public_code=item['id'])
        inst.name_ru = item['name_ru']
        inst.name_en = item['name_en']
        inst.save()
    for item in positions:
        item_inst_qnt = EmployeePosition.objects.filter(public_code=item['id']).count()
        if item_inst_qnt == 0:
            inst = EmployeePosition()
            inst.created_by = request.user
            inst.public_code = item['id']
        else:
            inst = EmployeePosition.objects.get(public_code=item['id'])
        inst.name_ru = item['name_ru']
        inst.name_en = item['name_en']
        inst.save()

    for item in industries:
        item_inst_qnt = Industry.objects.filter(public_code=item['id']).count()
        if item_inst_qnt == 0:
            inst = Industry()
            inst.created_by = request.user
            inst.public_code = item['id']
        else:
            inst = Industry.objects.get(public_code=item['id'])
        inst.name_ru = item['name_ru']
        inst.name_en = item['name_en']
        inst.save()

    for item in sex:
        item_inst_qnt = EmployeeGender.objects.filter(public_code=item['id']).count()
        if item_inst_qnt == 0:
            inst = EmployeeGender()
            inst.created_by = request.user
            inst.public_code = item['id']
        else:
            inst = EmployeeGender.objects.get(public_code=item['id'])
        inst.name_ru = item['name_ru']
        inst.name_en = item['name_en']
        inst.save()




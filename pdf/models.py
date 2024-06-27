import os.path

from django.db import models
from django.contrib.auth.models import User
import datetime


class ResearchTemplate(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    created_by = models.ForeignKey(User, default=None, null=True, on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.id}. {self.name}'

    class Meta:
        verbose_name_plural = 'Шаблоны опросника'
        verbose_name = 'Шаблон опросника'


class Section(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    created_by = models.ForeignKey(User, default=None, null=True, on_delete=models.PROTECT)
    edited_at = models.DateTimeField(auto_now=True, null=True)
    name = models.CharField(max_length=30, blank=False, null=False)
    # code = models.CharField(max_length=10, blank=True, null=True, default=None)

    def __str__(self):
        return f'{self.id}. {self.name}'

    class Meta:
        verbose_name_plural = 'Секции'
        verbose_name = 'Секция'


class ResearchTemplateSections(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    created_by = models.ForeignKey(User, default=None, null=True, on_delete=models.PROTECT)
    research_template = models.ForeignKey(ResearchTemplate, on_delete=models.PROTECT, default=None, null=True, blank=True)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, default=None, null=True, blank=True)
    position = models.IntegerField(null=False, default=0)

    def __str__(self):
        return f'{self.id}. research_template - {self.research_template.name} section - {self.section.name} position - {self.position}'

    class Meta:
        verbose_name_plural = 'Секции шаблона опросника'
        verbose_name = 'Секция шаблона опросника'


class Category(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    created_by = models.ForeignKey(User, default=None, null=True, on_delete=models.PROTECT)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, default=None, blank=True, null=True, verbose_name='Секция')
    name = models.CharField(max_length=100, blank=False, null=False)
    code = models.CharField(max_length=10, blank=True, null=True, default=None)
    for_validity = models.BooleanField(default=False, null=False)

    def __str__(self):
        # return f'категория - {self.name}'
        return f'ID. {self.id} категория - {self.name} | секция - {self.section} | code - {self.code}'

    class Meta:
        verbose_name_plural = 'Категории'
        verbose_name = 'Категория'


class CategoryQuestions(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    created_by = models.ForeignKey(User, default=None, null=True, on_delete=models.PROTECT)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, default=None, blank=True, null=True)
    text = models.TextField(blank=True, null=True, verbose_name='Текст вопроса')

    def __str__(self):
        # return f'категория - {self.name}'
        return f'ID. {self.id} категория - {self.category.name} | секция - {self.category.section.name}'

    class Meta:
        verbose_name_plural = 'Вопросы категории'
        verbose_name = 'Вопрос категории'


class QuestionAnswers(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    created_by = models.ForeignKey(User, default=None, null=True, on_delete=models.PROTECT)
    question = models.ForeignKey(CategoryQuestions, on_delete=models.CASCADE, default=None, blank=True, null=True)
    text = models.TextField(blank=True, null=True, verbose_name='Текст ответа')
    raw_point = models.IntegerField(null=False, default=0)
    position = models.IntegerField(null=False, default=0)

    def __str__(self):
        # return f'категория - {self.name}'
        return f'ID. {self.id} вопрос - {self.question.text} | категория - {self.question.category.name}'

    class Meta:
        verbose_name_plural = 'Ответы на вопросы'
        verbose_name = 'Ответ на вопрос'


class PointDescription(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    created_by = models.ForeignKey(User, default=None, null=True, on_delete=models.PROTECT)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=None, blank=True, null=True, verbose_name='Описание')
    value = models.IntegerField(null=False, default=0)
    text = models.TextField(blank=True, null=True, verbose_name='Русский')
    text_en = models.TextField(default=None, blank=True, null=True, verbose_name='Английский')

    def __str__(self):
        if self.text_en == '':
            return u'Англ отсутсвует'
        else:
            return f'{self.category.section.name} - {self.category.name} - {self.value}'

    class Meta:
        verbose_name_plural = 'Оисания баллов'
        verbose_name = 'Оисание баллов'


class Company(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    created_by = models.ForeignKey(User, default=None, null=True, on_delete=models.PROTECT)
    name = models.CharField(max_length=150, blank=False, null=False)
    version = models.IntegerField(null=True, default=0)
    active = models.BooleanField(default=True, null=False)
    email = models.CharField(max_length=100, blank=True, null=True, default=None)
    public_code = models.CharField(max_length=10, blank=False, null=False, default='')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Компании'
        verbose_name = 'Компания'


class Industry(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    created_by = models.ForeignKey(User, default=None, null=True, on_delete=models.PROTECT, related_name='Создано_пользователем')
    edited_at = models.DateTimeField(auto_now=True, null=True)
    edited_by = models.ForeignKey(User, default=None, null=True, on_delete=models.PROTECT, related_name='Изменено_пользователем')
    name_ru = models.CharField(max_length=100, blank=True, null=True)
    name_en = models.CharField(max_length=100, blank=True, null=True)
    public_code = models.CharField(max_length=10, blank=True, null=True, default='')

    def __str__(self):
        return self.name_ru

    class Meta:
        verbose_name_plural = 'Индустрии'
        verbose_name = 'Индустрия'


class EmployeeRole(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    created_by = models.ForeignKey(User, default=None, null=True, on_delete=models.PROTECT, related_name='Создано_пользователем_роль_сотрудника')
    edited_at = models.DateTimeField(auto_now=True, null=True)
    edited_by = models.ForeignKey(User, default=None, null=True, on_delete=models.PROTECT, related_name='Изменено_пользователем_роль_сотрудника')
    name_ru = models.CharField(max_length=100, blank=True, null=True)
    name_en = models.CharField(max_length=100, blank=True, null=True)
    public_code = models.CharField(max_length=10, blank=True, null=True, default='')

    def __str__(self):
        return self.name_ru

    class Meta:
        verbose_name_plural = 'Функции участников'
        verbose_name = 'Функция участника'


class EmployeeGender(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    created_by = models.ForeignKey(User, default=None, null=True, on_delete=models.PROTECT, related_name='Создано_пользователем_пол_сотрудника')
    edited_at = models.DateTimeField(auto_now=True, null=True)
    edited_by = models.ForeignKey(User, default=None, null=True, on_delete=models.PROTECT, related_name='Изменено_пользователем_пол_сотрудника')
    name_ru = models.CharField(max_length=100, blank=True, null=True)
    name_en = models.CharField(max_length=100, blank=True, null=True)
    public_code = models.CharField(max_length=10, blank=True, null=True, default='')

    def __str__(self):
        return self.name_ru

    class Meta:
        verbose_name_plural = 'Пол участников'
        verbose_name = 'Пол участника'


class EmployeePosition(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    created_by = models.ForeignKey(User, default=None, null=True, on_delete=models.PROTECT)
    name_ru = models.CharField(max_length=100, blank=True, null=True)
    name_en = models.CharField(max_length=100, blank=True, null=True)
    public_code = models.CharField(max_length=10, blank=True, null=True, default='')

    def __str__(self):
        return self.name_ru

    class Meta:
        verbose_name_plural = 'Должности участников'
        verbose_name = 'Должность участника'


class Employee(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, default=None, null=True, related_name='created_by_user')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, default=None, blank=True, null=True,
                             verbose_name='Пользователь', related_name='employee_user')
    name = models.CharField(max_length=100, blank=True, null=True)
    sex = models.ForeignKey(EmployeeGender, on_delete=models.PROTECT, default=None, blank=True, null=True, verbose_name='Пол')
    birth_year = models.IntegerField(blank=False, null=False)
    email = models.CharField(max_length=100, blank=True, null=False, default=None)
    company = models.ForeignKey(Company, on_delete=models.PROTECT, default=None, blank=True, null=True, verbose_name='Компания')
    role = models.ForeignKey(EmployeeRole, on_delete=models.PROTECT, default=1, blank=True, null=True, verbose_name='Роль участника')
    # role = models.CharField(max_length=100, blank=True, null=False, default=None)
    # position = models.CharField(max_length=100, blank=True, null=False, default=None)
    position = models.ForeignKey(EmployeePosition, on_delete=models.PROTECT, default=5, blank=True, null=True, verbose_name='Позиция участника')
    # industry = models.CharField(max_length=100, blank=True, null=False, default=None)
    industry = models.ForeignKey(Industry, on_delete=models.PROTECT, default=1, blank=True, null=True, verbose_name='Индустрия')
    company_admin = models.BooleanField(default=False, null=False)
    company_admin_active = models.BooleanField(default=False, null=False)

    def __str__(self):
        if self.name:
            # return f'{self.id}. {self.name} - {self.email} - role_id - {self.role.id}'
            return f'{self.id}. {self.name} - {self.email}'
        else:
            return f'{self.id}. {self.email}'
            # return f'{self.id}. {self.email} - role_id - {self.role.id}'

    class Meta:
        verbose_name_plural = 'Сотрудники (employee)'
        verbose_name = 'Сотрудник (employee)'


class Study(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, default=None, null=True)
    version = models.IntegerField(null=False, default=0)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, default=None, null=True)
    research_template = models.ForeignKey(ResearchTemplate, on_delete=models.PROTECT, default=None, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    public_code = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        # return f'{self.name} - {self.company.name}'
        return self.name

    class Meta:
        verbose_name_plural = 'Исследования (studies)'
        verbose_name = 'Исследование (study)'


class Participant(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, default=None, null=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, default=None, blank=True, null=True, verbose_name='Employee')
    started_at = models.DateTimeField(blank=True, null=True, default=None)
    completed_at = models.DateTimeField(blank=True, null=True, default=None)
    tos_accepted = models.BooleanField(default=False)
    study = models.ForeignKey(Study, on_delete=models.CASCADE, default=None, null=True, blank=True)
    invitation_sent = models.BooleanField(default=False)
    invitation_sent_datetime = models.DateTimeField(blank=True, null=True, default=None)
    invitation_code = models.TextField(default=None, null=True, blank=True)
    total_questions_qnt = models.IntegerField(default=0, null=True, blank=True)
    answered_questions_qnt = models.IntegerField(default=0, null=True, blank=True)
    current_percentage = models.IntegerField(default=0, null=True, blank=True)
    send_admin_notification_after_filling_up = models.BooleanField(default=False)
    send_report_to_participant_after_filling_up = models.BooleanField(default=False)

    def __str__(self):
        if self.employee and self.study:
            return f'{self.id}. {self.employee.name} - {self.employee.company.name} STUDY - {self.study.name}'
        else:
            return f'ID - {self.id}'

    class Meta:
        verbose_name_plural = 'Участники опроса'
        verbose_name = 'Участник опроса'


class Questionnaire(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    participant = models.ForeignKey(Participant, on_delete=models.PROTECT, default=None, blank=True, null=True)
    data_filled_up_by_participant = models.BooleanField(default=False)

    def __str__(self):
        # return f'{self.name} - {self.company.name}'
        return self.participant.employee.name

    class Meta:
        verbose_name_plural = 'Опросник респондента (questionnnaire)'
        verbose_name = 'Опросники респондентов (questionnnaire)'


class QuestionnaireQuestionAnswers(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.PROTECT, default=None, blank=True, null=True)
    question = models.ForeignKey(CategoryQuestions, on_delete=models.PROTECT, default=None, blank=True, null=True)
    answer = models.ForeignKey(QuestionAnswers, on_delete=models.PROTECT, default=None, blank=True, null=True)
    section = models.ForeignKey(Section, on_delete=models.PROTECT, default=None, blank=True, null=True)
    participant = models.ForeignKey(Participant, on_delete=models.PROTECT, default=None, blank=True, null=True)

    def __str__(self):
        return f'{self.questionnaire.participant.employee.name} - {self.question.category.section.name} -  {self.question.category.code}. {self.question.category.name} - очки = {self.answer.raw_point}'

    class Meta:
        verbose_name_plural = 'Опросник респондента_ответы (QuestionnaireQuestionAnswers)'
        verbose_name = 'Опросники респондентов_ответы (QuestionnaireQuestionAnswers)'


# class ParticipantQuestionGroups(models.Model):
#     created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
#     created_by = models.ForeignKey(User, on_delete=models.SET_NULL, default=None, null=True)
#     question_group_name = models.CharField(max_length=30, blank=True, null=True, default=None)
#     question_group_code = models.CharField(max_length=2, blank=True, null=True, default=None)
#     participant = models.ForeignKey(Participant, on_delete=models.CASCADE, default=None, null=True, blank=True)
#
#     def __str__(self):
#         return f'Группа вопросов - {self.question_group_name} Опросник - {self.participant}'
#
#     class Meta:
#         verbose_name_plural = 'Группы вопросов для участника'
#         verbose_name = 'Группа вопросов для участника'
#

class EmailSentToParticipant(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, default=None, null=True, blank=True)
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, default=None, null=True)
    type = models.CharField(max_length=30, blank=True, null=True, default=None)

    def __str__(self):
        return f'{self.participant.employee.name} - {self.type}'

    class Meta:
        verbose_name_plural = 'Письма отправленные'
        verbose_name = 'Письмо отправлено'


class AgeGenderGroup(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, default=None, null=True, blank=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    birth_year_start = models.IntegerField(blank=True, null=True)
    birth_year_end = models.IntegerField(blank=True, null=True)
    employee_gender = models.ForeignKey(EmployeeGender, on_delete=models.PROTECT, default=None, null=True)

    def __str__(self):
        return f'{self.name} -- {self.birth_year_start} - {self.birth_year_end}'

    class Meta:
        verbose_name_plural = 'Возрастные группы'
        verbose_name = 'Возрастная группа'


class RawToTPointsType(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, default=None, null=True, blank=True)
    is_default = models.BooleanField(default=False)
    name = models.CharField(max_length=100, blank=True, null=True)
    name_ru = models.CharField(max_length=200, blank=True, null=True)
    industry = models.ForeignKey(Industry, on_delete=models.PROTECT, default=None, null=True)
    employee_position = models.ForeignKey(EmployeePosition, on_delete=models.PROTECT, default=None, null=True)
    employee_role = models.ForeignKey(EmployeeRole, on_delete=models.PROTECT, default=None, null=True)
    age_gender_group = models.ForeignKey(AgeGenderGroup, on_delete=models.PROTECT, default=None, null=True)

    def __str__(self):
        return f'{self.name_ru}'

    class Meta:
        verbose_name_plural = 'Фильтры поправок'
        verbose_name = 'Фильтр поправки'


class RawToTPoints(models.Model):
    type = models.ForeignKey(RawToTPointsType, on_delete=models.CASCADE, default=None, blank=True, null=True)
    raw_points = models.IntegerField(null=False, default=0)
    t_point = models.IntegerField(null=False, default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=None, blank=True, null=True)

    def __str__(self):
        return f'{self.type.name_ru} - {self.category.section.name}- {self.category.name}  {self.raw_points} - {self.t_point}'

    class Meta:
        verbose_name_plural = 'Сырые данные в Т баллы'
        verbose_name = 'Сырые данные в Т баллы'


class Report(models.Model):
    added = models.DateTimeField(auto_now_add=True, null=True)
    code = models.CharField(max_length=30, blank=True, null=True)
    lie_points = models.IntegerField(null=False, default=0)
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, default=None, blank=True, null=True, verbose_name='Участник')
    file = models.FileField(upload_to='media/reportsPDF/', default=None)
    lang = models.CharField(max_length=2, blank=True, null=True, default=None)
    study = models.ForeignKey(Study, on_delete=models.CASCADE, default=None, null=True, blank=True)
    comments = models.TextField(default=None, blank=True, null=True, verbose_name='Комментарии индивидуальный отчет')

    def __str__(self):
        return f'{self.participant} - {self.file.name}'

    def filename(self):
        return os.path.basename(self.file.name)

    class Meta:
        verbose_name_plural = 'Индивидуальные отчеты'
        verbose_name = 'Индивидуальный отчет'


class ReportData(models.Model):
    report = models.ForeignKey(Report, on_delete=models.CASCADE, default=None, blank=True, null=True, verbose_name='Отчет')
    section_name = models.CharField(max_length=50, blank=True, null=True, default=None)
    section_code = models.CharField(max_length=2, blank=True, null=True, default=None)
    category_name = models.CharField(max_length=100, blank=True, null=True, default=None)
    category_code = models.CharField(max_length=5, blank=True, null=True, default=None)
    points = models.IntegerField(null=False, default=0)

    # def __str__(self):
    #     return f'{self.report.participant.employee.name} - {self.report.participant.employee.company.name} - {self.section_name} - {self.category_code} - {self.category_name} - {self.points}'
    def __str__(self):
        return f'{self.section_name} - {self.category_code} - {self.category_name} - {self.points} - {self.report.filename()}'

    class Meta:
        verbose_name_plural = 'Данные индивидуальных отчетов'
        verbose_name = 'Данные индивидуальных отчетов'


class ReportDataByCategories(models.Model):
    report = models.ForeignKey(Report, on_delete=models.CASCADE, default=None, blank=True, null=True, verbose_name='Отчет')
    section_name = models.CharField(max_length=50, blank=True, null=True, default=None)
    section_code = models.CharField(max_length=2, blank=True, null=True, default=None)
    category_name = models.CharField(max_length=100, blank=True, null=True, default=None)
    category_code = models.CharField(max_length=5, blank=True, null=True, default=None)
    t_points = models.IntegerField(null=False, default=0)

    # def __str__(self):
    #     return f'{self.report.participant.employee.name} - {self.report.participant.employee.company.name} - {self.section_name} - {self.category_code} - {self.category_name} - {self.points}'
    def __str__(self):
        return f'{self.section_name} - {self.category_code} - {self.category_name} - {self.t_points} - {self.report.filename()}'

    class Meta:
        verbose_name_plural = 'Данные индивидуальных отчетов'
        verbose_name = 'Данные индивидуальных отчетов'


class ReportGroup(models.Model):
    added = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    file = models.FileField(upload_to='media/reportsPDF/', default=None)
    lang = models.CharField(max_length=2, blank=True, null=True, default='ru')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, default=None, blank=True, null=True, verbose_name='Проект групповой отчет')
    comments = models.TextField(default=None, blank=True, null=True, verbose_name='Комментарии групповой отчет')

    def __str__(self):
        return f'{self.company} - {self.file.name}'

    class Meta:
        verbose_name_plural = 'Групповые отчеты'
        verbose_name = 'Групповой отчет'


class ReportGroupSquare(models.Model):
    added = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    report_group = models.ForeignKey(ReportGroup, on_delete=models.CASCADE, default=None, blank=True, null=True, verbose_name='Отчет групповой')
    square_name = models.CharField(max_length=30, blank=False, null=False, verbose_name='Квадрат_имя')
    square_code = models.CharField(max_length=30, blank=True, null=True, verbose_name='Квадрат_код', default=None)
    report = models.ForeignKey(Report, on_delete=models.CASCADE, default=None, blank=True, null=True, verbose_name='Отчет индивидуальный для группового')
    participant_group = models.CharField(max_length=300, blank=True, null=True, verbose_name='Группа участника', default=None)
    participant_group_color = models.CharField(max_length=20, blank=True, null=True, verbose_name='Цвет группы участника', default=None)
    bold = models.BooleanField(default=False)
    participant_number = models.IntegerField(null=False, default=0)

    def __str__(self):
        return f'{self.report.participant.employee.name} - {self.square_name}'

    class Meta:
        verbose_name_plural = 'Данные по квадратам групповых отчетов'
        verbose_name = 'Данные по квадрату групповых отчетов'


# class SquareName(models.Model):
#     created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
#     created_by = models.ForeignKey(User, on_delete=models.SET_NULL, default=None, null=True, blank=True)
#     code = models.CharField(max_length=30, blank=True, null=True)
#     name = models.CharField(max_length=30, blank=True, null=True)
#
#     def __str__(self):
#         return f'{self.code} - {self.name}'
#
#     class Meta:
#         verbose_name_plural = 'Имя/коды квадратов'
#         verbose_name = 'Имя/код квадрата'


class MatrixFilter(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, default=None, null=True, blank=True)
    square_code = models.CharField(max_length=30, blank=True, null=True)
    square_name = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f'{self.square_code} - {self.square_name}'

    class Meta:
        verbose_name_plural = 'Фильтры матриц'
        verbose_name = 'Фильтр матрицы'


class MatrixFilterCategory(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, default=None, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, default=None, blank=True, null=True)
    matrix_filter = models.ForeignKey(MatrixFilter, on_delete=models.CASCADE, default=None, blank=True, null=True)
    points_from = models.IntegerField(null=False, default=0)
    points_to = models.IntegerField(null=False, default=0)

    def __str__(self):
        return f'{self.matrix_filter.square_code}-{self.matrix_filter.square_name} -- {self.category.name} : {self.points_from} - {self.points_to}'

    class Meta:
        verbose_name_plural = 'Категории (шкалы) фильтров матриц'
        verbose_name = 'Категория (шкала) фильтра матрицы'


class MatrixFilterInclusiveEmployeePosition(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, default=None, null=True, blank=True)
    matrix_filter = models.ForeignKey(MatrixFilter, on_delete=models.CASCADE, default=None, blank=True, null=True)
    employee_position = models.ForeignKey(EmployeePosition, on_delete=models.PROTECT, default=None, null=True)

    def __str__(self):
        return f'{self.matrix_filter.square_code}-{self.matrix_filter.square_name} -- {self.employee_position.name_ru}'

    class Meta:
        verbose_name_plural = 'Должности, включенные в фильтры матриц'
        verbose_name = 'Должность, включенная в фильтр матрицы'


class MatrixFilterParticipantNotDistributed(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, default=None, null=True, blank=True)
    square_code = models.CharField(max_length=30, blank=True, null=True)
    square_name = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return f'{self.created_at} - {self.created_by.username}'

    class Meta:
        verbose_name_plural = 'Фильтры матриц (если ни в один квадрет не попал)'
        verbose_name = 'Фильтр матрицы (если ни в один квадрет не попал)'


class MatrixFilterParticipantNotDistributedEmployeePosition(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, default=None, null=True, blank=True)
    matrix_filter = models.ForeignKey(MatrixFilterParticipantNotDistributed, on_delete=models.CASCADE, default=None, blank=True, null=True)
    employee_position = models.ForeignKey(EmployeePosition, on_delete=models.PROTECT, default=None, null=True)

    def __str__(self):
        return f'{self.matrix_filter.id}-{self.matrix_filter.created_at} -- {self.employee_position.name_ru}'

    class Meta:
        verbose_name_plural = 'Должности, включенные в фильтры матриц'
        verbose_name = 'Должность, включенная в фильтр матрицы'


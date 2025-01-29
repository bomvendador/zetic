import os.path

from django.db import models
from django.contrib.auth.models import User
import datetime
from django.utils import timezone
# from positions import PositionField


class ResearchTemplate(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    created_by = models.ForeignKey(User, default=None, null=True, on_delete=models.PROTECT)
    by_default = models.BooleanField(default=False)

    def __str__(self):
        return f'[{timezone.localtime(self.created_at).strftime("%d.%m.%Y %H:%M:%S")}] : {self.id}. {self.name}'

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
        return f'[{timezone.localtime(self.created_at).strftime("%d.%m.%Y %H:%M:%S")}] : {self.id}. {self.name}'

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
        return f'[{timezone.localtime(self.created_at).strftime("%d.%m.%Y %H:%M:%S")}] : {self.id}. research_template - {self.research_template.name} section - {self.section.name} position - {self.position}'

    class Meta:
        verbose_name_plural = 'Секции шаблона опросника'
        verbose_name = 'Секция шаблона опросника'


class Category(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    created_by = models.ForeignKey(User, default=None, null=True, on_delete=models.PROTECT)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, default=None, blank=True, null=True, verbose_name='Секция')
    name = models.CharField(max_length=100, blank=False, null=False)
    code = models.CharField(max_length=10, blank=True, default=None, null=True)
    for_validity = models.BooleanField(default=False, null=False)

    def __str__(self):
        return f'[{timezone.localtime(self.created_at).strftime("%d.%m.%Y %H:%M:%S")}] : {self.id} категория - {self.name} | секция - {self.section} | code - {self.code}'

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
        return f'[{timezone.localtime(self.created_at).strftime("%d.%m.%Y %H:%M:%S")}] : {self.id} категория - {self.category.name} | секция - {self.category.section.name}'

    class Meta:
        verbose_name_plural = 'Вопросы категории'
        verbose_name = 'Вопрос категории'


class QuestionAnswers(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    created_by = models.ForeignKey(User, default=None, null=True, on_delete=models.PROTECT)
    question = models.ForeignKey(CategoryQuestions, on_delete=models.CASCADE, default=None, blank=True, null=True)
    text = models.TextField(blank=True, verbose_name='Текст ответа', null=True)
    raw_point = models.IntegerField(null=False, default=0)
    position = models.IntegerField(null=False, default=0)

    def __str__(self):
        # return f'категория - {self.name}'
        return f'[{timezone.localtime(self.created_at).strftime("%d.%m.%Y %H:%M:%S")}] : {self.id} вопрос - {self.question.text} | категория - {self.question.category.name}'

    class Meta:
        verbose_name_plural = 'Ответы на вопросы'
        verbose_name = 'Ответ на вопрос'


class PointDescription(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    created_by = models.ForeignKey(User, default=None, null=True, on_delete=models.PROTECT)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=None, blank=True, null=True, verbose_name='Описание')
    value = models.IntegerField(null=False, default=0)
    text = models.TextField(blank=True, verbose_name='Русский', null=True)
    text_en = models.TextField(default=None, blank=True, verbose_name='Английский', null=True)

    def __str__(self):
        if self.text_en == '':
            return u'Англ отсутсвует'
        else:
            return f'[{timezone.localtime(self.created_at).strftime("%d.%m.%Y %H:%M:%S")}] : {self.id}. {self.category.section.name} - {self.category.name} - {self.value}'

    class Meta:
        verbose_name_plural = 'Оисания баллов'
        verbose_name = 'Оисание баллов'


class Company(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    created_by = models.ForeignKey(User, default=None, null=True, on_delete=models.PROTECT)
    name = models.CharField(max_length=150, blank=False, null=False)
    version = models.IntegerField(null=True, default=0)
    active = models.BooleanField(default=True, null=False)
    email = models.CharField(max_length=100, blank=True, default=None, null=True)
    public_code = models.CharField(max_length=10, blank=False, null=False, default='')
    demo_status = models.BooleanField(default=True, null=False)
    demo_status_questionnaires_limit = models.IntegerField(null=True, default=3)

    def __str__(self):
        return f'[{timezone.localtime(self.created_at).strftime("%d.%m.%Y %H:%M:%S")}] : {self.id}. {self.name}'

    class Meta:
        verbose_name_plural = 'Компании'
        verbose_name = 'Компания'


class IndividualReportAllowedOptions(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    created_by = models.ForeignKey(User, default=None, null=True, on_delete=models.PROTECT)
    name = models.CharField(max_length=100, blank=False, null=False, default='')

    def __str__(self):
        return f'[{timezone.localtime(self.created_at).strftime("%d.%m.%Y %H:%M:%S")}] : {self.id}. {self.name}'

    class Meta:
        verbose_name_plural = 'Опции в личных отчетах (IndividualReportAllowedOptions)'
        verbose_name = 'Опция в личных отчетах (IndividualReportAllowedOptions)'


class CompanyIndividualReportAllowedOptions(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    created_by = models.ForeignKey(User, default=None, null=True, on_delete=models.PROTECT)
    company = models.ForeignKey(Company, default=None, null=True, on_delete=models.CASCADE)
    option = models.ForeignKey(IndividualReportAllowedOptions, default=None, null=True, on_delete=models.CASCADE)
    value = models.BooleanField(default=True, null=False)

    def __str__(self):
        return f'[{timezone.localtime(self.created_at).strftime("%d.%m.%Y %H:%M:%S")}] : {self.id}. {self.company.name} - {self.option.name}'

    class Meta:
        verbose_name_plural = 'Опции компании в личных отчетах (CompanyIndividualReportAllowedOptions)'
        verbose_name = 'Опция компании в личных отчетах (CompanyIndividualReportAllowedOptions)'


class GroupReportAllowedOptions(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    created_by = models.ForeignKey(User, default=None, null=True, on_delete=models.PROTECT)
    name = models.CharField(max_length=100, blank=False, null=False, default='')

    def __str__(self):
        return f'[{timezone.localtime(self.created_at).strftime("%d.%m.%Y %H:%M:%S")}] : {self.id}. {self.name}'

    class Meta:
        verbose_name_plural = 'Опции в группоовых отчетах (GroupReportAllowedOptions)'
        verbose_name = 'Опция в группоовых отчетах (GroupReportAllowedOptions)'


class CompanyGroupReportAllowedOptions(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    created_by = models.ForeignKey(User, default=None, null=True, on_delete=models.PROTECT)
    company = models.ForeignKey(Company, default=None, null=True, on_delete=models.CASCADE)
    option = models.ForeignKey(GroupReportAllowedOptions, default=None, null=True, on_delete=models.CASCADE)
    value = models.BooleanField(default=True, null=False)

    def __str__(self):
        return f'[{timezone.localtime(self.created_at).strftime("%d.%m.%Y %H:%M:%S")}] : {self.id}. {self.company.name} - {self.option.name}'

    class Meta:
        verbose_name_plural = 'Опции компании в группоовых отчетах (CompanyGroupReportAllowedOptions)'
        verbose_name = 'Опция компании в группоовых отчетах (CompanyGroupReportAllowedOptions)'


class CompanySelfQuestionnaireLink(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    created_by = models.ForeignKey(User, default=None, null=True, on_delete=models.PROTECT)
    company = models.ForeignKey(Company, default=None, null=True, on_delete=models.PROTECT)
    research_template = models.ForeignKey(ResearchTemplate, default=None, null=True, on_delete=models.PROTECT)
    code = models.CharField(max_length=20, blank=False, null=False, default='')
    active = models.BooleanField(default=True, null=False)

    def __str__(self):
        return f'[{timezone.localtime(self.created_at).strftime("%d.%m.%Y %H:%M:%S")}] : {self.id}. {self.company.name}'

    class Meta:
        verbose_name_plural = 'Ссылки компаний для создания опросников (CompanySelfQuestionnaireLink)'
        verbose_name = 'Ссылка компании для создания опросников (CompanySelfQuestionnaireLink)'


class Industry(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    created_by = models.ForeignKey(User, default=None, null=True, on_delete=models.PROTECT, related_name='Создано_пользователем')
    edited_at = models.DateTimeField(auto_now=True, null=True)
    edited_by = models.ForeignKey(User, default=None, null=True, on_delete=models.PROTECT, related_name='Изменено_пользователем')
    name_ru = models.CharField(max_length=100, blank=True, null=True)
    name_en = models.CharField(max_length=100, blank=True, null=True)
    public_code = models.CharField(max_length=10, blank=True, default='', null=True)

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
    public_code = models.CharField(max_length=10, blank=True, default='', null=True)

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
    public_code = models.CharField(max_length=10, blank=True, default='', null=True)

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
    public_code = models.CharField(max_length=10, blank=True, default='', null=True)

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
    birth_year = models.IntegerField(blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=False, default=None)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, default=None, blank=True, null=True, verbose_name='Компания')
    role = models.ForeignKey(EmployeeRole, on_delete=models.PROTECT, default=None, blank=True, null=True, verbose_name='Роль участника')
    # position = models.CharField(max_length=100, blank=True, null=False, default=None)
    position = models.ForeignKey(EmployeePosition, on_delete=models.PROTECT, default=None, blank=True, null=True, verbose_name='Позиция участника')
    industry = models.ForeignKey(Industry, on_delete=models.PROTECT, default=None, blank=True, null=True, verbose_name='Индустрия')
    company_admin = models.BooleanField(default=False, null=False)
    company_admin_active = models.BooleanField(default=False, null=False)

    def __str__(self):
        if self.name:
            return f'[{timezone.localtime(self.created_at).strftime("%d.%m.%Y %H:%M:%S")}] : {self.id}. {self.name} - {self.email}'
        else:
            return f'[{timezone.localtime(self.created_at).strftime("%d.%m.%Y %H:%M:%S")}] : {self.id}. {self.email}'

    class Meta:
        verbose_name_plural = 'Сотрудники (employee)'
        verbose_name = 'Сотрудник (employee)'


class CompanyReportMadeNotificationReceivers(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    created_by = models.ForeignKey(User, default=None, null=True, on_delete=models.PROTECT)
    company = models.ForeignKey(Company, default=None, null=True, on_delete=models.PROTECT)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, default=None, blank=True, null=True, verbose_name='Employee_notification_receivers')

    def __str__(self):
        return f'[{timezone.localtime(self.created_at).strftime("%d.%m.%Y %H:%M:%S")}] : {self.id}. {self.company.name} - {self.employee.name}'

    class Meta:
        verbose_name_plural = 'Сотрудники-получатели уведомления о созданном отчете'
        verbose_name = 'Сотрудник-получатель уведомления о созданном отчете'


class UsersReportMadeNotificationReceivers(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    created_by = models.ForeignKey(User, default=None, null=True, on_delete=models.PROTECT, related_name='Created_by')
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, blank=True, null=True, verbose_name='User_notification_receivers')

    def __str__(self):
        return f'[{timezone.localtime(self.created_at).strftime("%d.%m.%Y %H:%M:%S")}] : {self.id}. {self.user.username} - {self.user.first_name}'

    class Meta:
        verbose_name_plural = 'Пользователи-получатели уведомления о созданном отчете'
        verbose_name = 'Пользователь-получатель уведомления о созданном отчете'


class Study(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, default=None, null=True)
    version = models.IntegerField(null=False, default=0)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, default=None, null=True)
    research_template = models.ForeignKey(ResearchTemplate, on_delete=models.PROTECT, default=None, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    public_code = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        if self.company:
            return f'[{timezone.localtime(self.created_at).strftime("%d.%m.%Y %H:%M:%S")}] : {self.name} - {self.company.id}.{self.company.name}'
        else:
            return self.name

    class Meta:
        verbose_name_plural = 'Исследования (studies)'
        verbose_name = 'Исследование (study)'


class StudyIndividualReportAllowedOptions(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    created_by = models.ForeignKey(User, default=None, null=True, on_delete=models.PROTECT)
    study = models.ForeignKey(Study, default=None, null=True, on_delete=models.CASCADE)
    option = models.ForeignKey(IndividualReportAllowedOptions, default=None, null=True, on_delete=models.CASCADE)
    value = models.BooleanField(default=True, null=False)

    def __str__(self):
        return f'[{timezone.localtime(self.created_at).strftime("%d.%m.%Y %H:%M:%S")}] : {self.id}. {self.study.name} - {self.option.name}'

    class Meta:
        verbose_name_plural = 'Опции исследований в личных отчетах (StudyIndividualReportAllowedOptions)'
        verbose_name = 'Опция исследования в личном отчетах (StudyIndividualReportAllowedOptions)'


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
    invitation_code = models.TextField(default=None, blank=True, null=True)
    total_questions_qnt = models.IntegerField(default=0, null=True, blank=True)
    answered_questions_qnt = models.IntegerField(default=0, null=True, blank=True)
    current_percentage = models.IntegerField(default=0, null=True, blank=True)
    send_admin_notification_after_filling_up = models.BooleanField(default=False)
    send_report_to_participant_after_filling_up = models.BooleanField(default=False)

    def __str__(self):
        if self.employee and self.study:
            return f'[{timezone.localtime(self.created_at).strftime("%d.%m.%Y %H:%M:%S")}] : {self.id}. {self.employee.name} - {self.employee.company.name} STUDY - {self.study.name}'
        else:
            return f'ID - {self.id}'

    def question_answered_percentage(self):
        if self.answered_questions_qnt == 0 or self.answered_questions_qnt is None:
            text = 0
        else:
            text = round(self.answered_questions_qnt / self.total_questions_qnt * 100)
        return f'{text}%'

    class Meta:
        verbose_name_plural = 'Участники опроса'
        verbose_name = 'Участник опроса'


class ParticipantIndividualReportAllowedOptions(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    created_by = models.ForeignKey(User, default=None, null=True, on_delete=models.PROTECT)
    participant = models.ForeignKey(Participant, default=None, null=True, on_delete=models.CASCADE)
    option = models.ForeignKey(IndividualReportAllowedOptions, default=None, null=True, on_delete=models.CASCADE)
    value = models.BooleanField(default=True, null=False)

    def __str__(self):
        return f'[{timezone.localtime(self.created_at).strftime("%d.%m.%Y %H:%M:%S")}] : {self.id}. {self.participant.employee.name} - {self.option.name}'

    class Meta:
        verbose_name_plural = 'Опции участников в личных отчетах (ParticipantIndividualReportAllowedOptions)'
        verbose_name = 'Опция участника в личном отчетах (ParticipantIndividualReportAllowedOptions)'


# class Consultant(models.Model):
#     created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
#     created_by = models.ForeignKey(User, on_delete=models.SET_NULL, default=None, null=True)
#     user = models.ForeignKey(User, on_delete=models.PROTECT, default=None, blank=True, null=True, related_name='Консультант')
#
#     def __str__(self):
#         return f'{self.id}. {self.user.first_name}'
#
#     class Meta:
#         verbose_name_plural = 'Консультант (Consultant)'
#         verbose_name = 'Консультанты (Consultan)'
#

class ConsultantCompany(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, default=None, null=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, default=None, blank=True, null=True, related_name='UserConsultantCompany')
    company = models.ForeignKey(Company, on_delete=models.PROTECT, default=None, blank=True, null=True)

    def __str__(self):
        # return f'{self.name} - {self.company.name}'
        return f'[{timezone.localtime(self.created_at).strftime("%d.%m.%Y %H:%M:%S")}] : {self.id}. {self.user.first_name} - {self.company.name}'

    class Meta:
        verbose_name_plural = 'Компания консультанта (ConsultantCompany)'
        verbose_name = 'Компании консультантов (ConsultantCompany)'


class ConsultantStudy(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, default=None, null=True)
    study = models.ForeignKey(Study, on_delete=models.PROTECT, default=None, blank=True, null=True)
    consultant_company = models.ForeignKey(ConsultantCompany, on_delete=models.CASCADE, default=None, blank=True, null=True)

    def __str__(self):
        # return f'{self.name} - {self.company.name}'
        return f'[{timezone.localtime(self.created_at).strftime("%d.%m.%Y %H:%M:%S")}] : {self.id}. {self.user.first_name} - {self.study.name}'

    class Meta:
        verbose_name_plural = 'Исследование консультанта (ConsultantStudy)'
        verbose_name = 'Исследования консультантов (ConsultantStudy)'


class ConsultantForm(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, default=None, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, default=None, blank=True, null=True, related_name='UserConsultantForm')
    special_comments = models.TextField(default=None, blank=True, verbose_name='Специальные комментарии', null=True)
    risks = models.TextField(default=None, blank=True, verbose_name='Риски', null=True)
    career_track = models.TextField(default=None, blank=True, verbose_name='Карьерный трек', null=True)

    def __str__(self):
        return f'[{timezone.localtime(self.created_at).strftime("%d.%m.%Y %H:%M:%S")}] : {self.id}. {self.user.first_name} - {self.participant.employee.name}'

    class Meta:
        verbose_name_plural = 'Анкета консультанта (ConsultantForm)'
        verbose_name = 'Анкеты консультантов (ConsultantForm)'


class ConsultantFormResources(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, default=None, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    consultant_form = models.ForeignKey(ConsultantForm, on_delete=models.CASCADE, default=None, null=True)

    def __str__(self):
        return f'[{timezone.localtime(self.created_at).strftime("%d.%m.%Y %H:%M:%S")}] : {self.id}. {self.name} - {self.consultant_form.participant.employee.name}'

    class Meta:
        verbose_name_plural = 'Анкета консультанта - Ресурс (ConsultantFormResources)'
        verbose_name = 'Анкеты консультантов - Ресурсы (ConsultantFormResources)'


class ConsultantFormResourcesComments(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, default=None, null=True)
    consultant_form_resource = models.ForeignKey(ConsultantFormResources, on_delete=models.CASCADE, default=None, null=True)
    text = models.TextField(default=None, blank=True, verbose_name='Ресурс_текст_коммента', null=True)

    def __str__(self):
        return f'[{timezone.localtime(self.created_at).strftime("%d.%m.%Y %H:%M:%S")}] : {self.id}. {self.consultant_form_resource.name}'

    class Meta:
        verbose_name_plural = 'Анкета консультанта - Ресурс_коммент (ConsultantFormResourcesComments)'
        verbose_name = 'Анкеты консультантов - Ресурсы_комменты (ConsultantFormResourcesComments)'


class ConsultantFormGrowthZone(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, default=None, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    consultant_form = models.ForeignKey(ConsultantForm, on_delete=models.CASCADE, default=None, null=True)

    def __str__(self):
        return f'[{timezone.localtime(self.created_at).strftime("%d.%m.%Y %H:%M:%S")}] : {self.id}. {self.name} - {self.consultant_form.participant.employee.name}'

    class Meta:
        verbose_name_plural = 'Анкета консультанта - Ресурс (ConsultantFormResources)'
        verbose_name = 'Анкеты консультантов - Ресурсы (ConsultantFormResources)'


class ConsultantFormGrowthZoneComments(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, default=None, null=True)
    consultant_form_growth_zone = models.ForeignKey(ConsultantFormGrowthZone, on_delete=models.CASCADE, default=None, null=True)
    text = models.TextField(default=None, blank=True, verbose_name='Зона роста_текст_коммента', null=True)

    def __str__(self):
        return f'[{timezone.localtime(self.created_at).strftime("%d.%m.%Y %H:%M:%S")}] : {self.id}. {self.consultant_form_growth_zone.name}'

    class Meta:
        verbose_name_plural = 'Анкета консультанта - Зона роста_коммент (ConsultantFormGrowthZoneComments)'
        verbose_name = 'Анкеты консультантов - Зона роста_комменты (ConsultantFormGrowthZoneComments)'


class ConsultantFormEmailSentToParticipant(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, default=None, null=True, blank=True)
    consultant_form = models.ForeignKey(ConsultantForm, on_delete=models.CASCADE, default=None, null=True)

    def __str__(self):
        return f'[{timezone.localtime(self.created_at).strftime("%d.%m.%Y %H:%M:%S")}] : {self.consultant_form.participant.employee.name} - {self.created_at}'

    class Meta:
        verbose_name_plural = 'Анкеты консультанта Отправления респонденту (ConsultantFormEmailSentToParticipant)'
        verbose_name = 'Анкета консультанта Отправление респонденту (ConsultantFormEmailSentToParticipant)'


class Questionnaire(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, default=None, blank=True, null=True)
    data_filled_up_by_participant = models.BooleanField(default=False)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f'[{timezone.localtime(self.created_at).strftime("%d.%m.%Y %H:%M:%S")}] : {self.id}. {self.participant.employee.name}'

    class Meta:
        verbose_name_plural = 'Опросник респондента (questionnnaire)'
        verbose_name = 'Опросники респондентов (questionnnaire)'


class QuestionnaireQuestionAnswers(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE, default=None, blank=True, null=True)
    question = models.ForeignKey(CategoryQuestions, on_delete=models.PROTECT, default=None, blank=True, null=True)
    answer = models.ForeignKey(QuestionAnswers, on_delete=models.PROTECT, default=None, blank=True, null=True)
    section = models.ForeignKey(Section, on_delete=models.PROTECT, default=None, blank=True, null=True)
    participant = models.ForeignKey(Participant, on_delete=models.PROTECT, default=None, blank=True, null=True)

    def __str__(self):
        return f'[{timezone.localtime(self.created_at).strftime("%d.%m.%Y %H:%M:%S")}] ID - {self.id}. ({self.questionnaire.participant.total_questions_qnt}/{self.questionnaire.participant.answered_questions_qnt}){self.questionnaire.participant.employee.name} - {self.question.category.section.name} -  {self.question.category.code}. {self.question.category.name} - очки = {self.answer.raw_point} ответ - {self.answer.text}'

    class Meta:
        verbose_name_plural = 'Опросник респондента_ответы (QuestionnaireQuestionAnswers)'
        verbose_name = 'Опросники респондентов_ответы (QuestionnaireQuestionAnswers)'


class QuestionnaireVisits(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE, default=None, blank=True, null=True)

    def __str__(self):
        return f'[{timezone.localtime(self.created_at).strftime("%d.%m.%Y %H:%M:%S")}] : {self.id}. {self.questionnaire.participant.employee.name}'

    class Meta:
        verbose_name_plural = 'Опросник время посещения (QuestionnaireVisits)'
        verbose_name = 'Опросники время посещения (QuestionnaireVisits)'


class Project(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, default=None, null=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, default=None, null=True, blank=True)

    def __str__(self):
        return f'[{timezone.localtime(self.created_at).strftime("%d.%m.%Y %H:%M:%S")}] : {self.id}. {self.name} - {self.company.name}'

    class Meta:
        verbose_name_plural = 'Проекты'
        verbose_name = 'Проект'


class ProjectStudy(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, default=None, null=True)
    study = models.ForeignKey(Study, on_delete=models.CASCADE, default=None, null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, default=None, null=True, blank=True)

    def __str__(self):
        return f'[{timezone.localtime(self.created_at).strftime("%d.%m.%Y %H:%M:%S")}] : {self.id}. {self.study.name} - {self.study.company.name}'

    class Meta:
        verbose_name_plural = 'Исследования (Study) проектов'
        verbose_name = 'Исследование (Study) проекта'


class EmailSentToParticipant(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, default=None, null=True, blank=True)
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, default=None, null=True)
    type = models.CharField(max_length=30, blank=True, default=None, null=True)

    def __str__(self):
        return f'[{timezone.localtime(self.created_at).strftime("%d.%m.%Y %H:%M:%S")}] : {self.participant.employee.name} - {self.type}'

    class Meta:
        verbose_name_plural = 'Письма отправленные'
        verbose_name = 'Письмо отправлено'


class AgeGenderGroup(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, default=None, null=True, blank=True)
    name = models.CharField(max_length=100, blank=True, default=None, null=True)
    birth_year_start = models.IntegerField(blank=True, null=True)
    birth_year_end = models.IntegerField(blank=True, null=True)
    employee_gender = models.ForeignKey(EmployeeGender, on_delete=models.PROTECT, default=None, null=True)

    def __str__(self):
        return f'[{timezone.localtime(self.created_at).strftime("%d.%m.%Y %H:%M:%S")}] : {self.name} -- {self.birth_year_start} - {self.birth_year_end}'

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
        return f'[{timezone.localtime(self.created_at).strftime("%d.%m.%Y %H:%M:%S")}] : {self.id}. {self.name_ru}'

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
    lang = models.CharField(max_length=2, blank=True, default=None, null=True)
    study = models.ForeignKey(Study, on_delete=models.CASCADE, default=None, null=True, blank=True)
    comments = models.TextField(default=None, blank=True, verbose_name='Комментарии индивидуальный отчет', null=True)
    primary = models.BooleanField(default=True)
    type = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return f'[{timezone.localtime(self.added).strftime("%d.%m.%Y %H:%M:%S")}] : {self.id}. {self.participant} - {self.file.name}'

    def filename(self):
        return os.path.basename(self.file.name)

    class Meta:
        verbose_name_plural = 'Индивидуальные отчеты (Report)'
        verbose_name = 'Индивидуальный отчет (Report)'


class ReportData(models.Model):
    report = models.ForeignKey(Report, on_delete=models.CASCADE, default=None, blank=True, null=True, verbose_name='Отчет')
    section_name = models.CharField(max_length=50, blank=True, default=None, null=True)
    section_code = models.CharField(max_length=2, blank=True, default=None, null=True)
    category_name = models.CharField(max_length=100, blank=True, default=None, null=True)
    category_code = models.CharField(max_length=5, blank=True, default=None, null=True)
    points = models.IntegerField(null=False, default=0)

    def __str__(self):
        return f'{self.section_name} - {self.category_code} - {self.category_name} - {self.points} - {self.report.filename()}'

    class Meta:
        verbose_name_plural = 'Данные индивидуальных отчетов'
        verbose_name = 'Данные индивидуальных отчетов'


class ReportDataByCategories(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    report = models.ForeignKey(Report, on_delete=models.CASCADE, default=None, blank=True, null=True, verbose_name='Отчет')
    section_name = models.CharField(max_length=50, blank=True, default=None, null=True)
    section_code = models.CharField(max_length=2, blank=True, default=None, null=True)
    category_name = models.CharField(max_length=100, blank=True, default=None, null=True)
    category_code = models.CharField(max_length=5, blank=True, default=None, null=True)
    t_points = models.IntegerField(null=False, default=0)

    def __str__(self):
        return f'[{timezone.localtime(self.created_at).strftime("%d.%m.%Y %H:%M:%S")}] : {self.id}. {self.report.participant.employee.name} - {self.section_name} - {self.category_code} - {self.category_name} - {self.t_points}'

    class Meta:
        verbose_name_plural = 'Данные индивидуальных отчетов по категориям (ReportDataByCategories)'
        verbose_name = 'Данные индивидуальных отчетов по категориям (ReportDataByCategories)'


class ReportGroup(models.Model):
    added = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    file = models.FileField(upload_to='media/reportsPDF/', default=None, max_length=254)
    lang = models.CharField(max_length=2, blank=True, default='ru', null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, default=None, blank=True, null=True, verbose_name='Проект групповой отчет')
    comments = models.TextField(default=None, blank=True, verbose_name='Комментарии групповой отчет', null=True)

    def __str__(self):
        return f'[{timezone.localtime(self.added).strftime("%d.%m.%Y %H:%M:%S")}] : {self.id}. {self.company} - {self.file.name}'

    class Meta:
        verbose_name_plural = 'Групповые отчеты'
        verbose_name = 'Групповой отчет'


class ReportGroupSquare(models.Model):
    added = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    report_group = models.ForeignKey(ReportGroup, on_delete=models.CASCADE, default=None, blank=True, null=True, verbose_name='Отчет групповой')
    square_name = models.CharField(max_length=30, blank=False, null=False, verbose_name='Квадрат_имя')
    square_code = models.CharField(max_length=30, blank=True, verbose_name='Квадрат_код', default=None, null=True)
    report = models.ForeignKey(Report, on_delete=models.CASCADE, default=None, blank=True, null=True, verbose_name='Отчет индивидуальный для группового')
    participant_group = models.CharField(max_length=300, blank=True, verbose_name='Группа участника', default=None, null=True)
    participant_group_color = models.CharField(max_length=20, blank=True, verbose_name='Цвет группы участника', default=None, null=True)
    bold = models.BooleanField(default=False)
    participant_number = models.IntegerField(null=False, default=0)

    def __str__(self):
        return f'[{timezone.localtime(self.added).strftime("%d.%m.%Y %H:%M:%S")}] : {self.id}. {self.report.participant.employee.name} - {self.square_name}'

    class Meta:
        verbose_name_plural = 'Данные по квадратам групповых отчетов (ReportGroupSquare)'
        verbose_name = 'Данные по квадрату групповых отчетов (ReportGroupSquare)'


class ProjectParticipants(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, default=None, null=True)
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, default=None, null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, default=None, null=True, blank=True)
    report_group = models.ForeignKey(ReportGroup, on_delete=models.CASCADE, default=None, null=True, blank=True)

    def __str__(self):
        return f'[{timezone.localtime(self.created_at).strftime("%d.%m.%Y %H:%M:%S")}] : {self.id}. {self.participant.employee.name} - {self.project.name}'

    class Meta:
        verbose_name_plural = 'Участники проектов'
        verbose_name = 'Участник проекта'


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
        return f'[{timezone.localtime(self.created_at).strftime("%d.%m.%Y %H:%M:%S")}] : {self.id}. {self.square_code} - {self.square_name}'

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
        return f'[{timezone.localtime(self.created_at).strftime("%d.%m.%Y %H:%M:%S")}] : {self.id}. {self.matrix_filter.square_code}-{self.matrix_filter.square_name} -- {self.category.name} : {self.points_from} - {self.points_to}'

    class Meta:
        verbose_name_plural = 'Категории (шкалы) фильтров матриц'
        verbose_name = 'Категория (шкала) фильтра матрицы'


class MatrixFilterInclusiveEmployeePosition(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, default=None, null=True, blank=True)
    matrix_filter = models.ForeignKey(MatrixFilter, on_delete=models.CASCADE, default=None, blank=True, null=True)
    employee_position = models.ForeignKey(EmployeePosition, on_delete=models.PROTECT, default=None, null=True)

    def __str__(self):
        return f'[{timezone.localtime(self.created_at).strftime("%d.%m.%Y %H:%M:%S")}] : {self.id}. {self.matrix_filter.square_code}-{self.matrix_filter.square_name} -- {self.employee_position.name_ru}'

    class Meta:
        verbose_name_plural = 'Должности, включенные в фильтры матриц'
        verbose_name = 'Должность, включенная в фильтр матрицы'


class MatrixFilterParticipantNotDistributed(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, default=None, null=True, blank=True)
    square_code = models.CharField(max_length=30, blank=True, null=True)
    square_name = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return f'[{timezone.localtime(self.created_at).strftime("%d.%m.%Y %H:%M:%S")}] : {self.id}. {self.created_by.username}'

    class Meta:
        verbose_name_plural = 'Фильтры матриц (если ни в один квадрет не попал)'
        verbose_name = 'Фильтр матрицы (если ни в один квадрет не попал)'


class MatrixFilterParticipantNotDistributedEmployeePosition(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, default=None, null=True, blank=True)
    matrix_filter = models.ForeignKey(MatrixFilterParticipantNotDistributed, on_delete=models.CASCADE, default=None, blank=True, null=True)
    employee_position = models.ForeignKey(EmployeePosition, on_delete=models.PROTECT, default=None, null=True)

    def __str__(self):
        return f'[{timezone.localtime(self.created_at).strftime("%d.%m.%Y %H:%M:%S")}] : {self.id}. {self.matrix_filter.id}-{self.matrix_filter.created_at} -- {self.employee_position.name_ru}'

    class Meta:
        verbose_name_plural = 'Должности, для нераспределенных в фильтры матриц'
        verbose_name = 'Должность, для нераспределенных в фильтр матрицы'


class IndividualReportPointsDescriptionFilter(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, default=None, null=True, blank=True)
    name = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f'[{timezone.localtime(self.created_at).strftime("%d.%m.%Y %H:%M:%S")}] : {self.id}. {self.name}'

    class Meta:
        verbose_name_plural = 'Фильтры Описания баллов (личные отчеты)'
        verbose_name = 'Фильтр Описания баллов (личные отчеты)'


class IndividualReportPointsDescriptionFilterCategory(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, default=None, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, default=None, blank=True, null=True)
    filter = models.ForeignKey(IndividualReportPointsDescriptionFilter, on_delete=models.CASCADE, default=None, blank=True, null=True)
    points_from = models.IntegerField(null=False, default=0)
    points_to = models.IntegerField(null=False, default=0)

    def __str__(self):
        return f'[{timezone.localtime(self.created_at).strftime("%d.%m.%Y %H:%M:%S")}] : {self.id}. {self.filter.name}'

    class Meta:
        verbose_name_plural = 'Фильтры описания баллов: Категории (шкалы)  (личные отчеты)'
        verbose_name = 'Фильтр описания баллов: Категория (шкалы) (личные отчеты)'


class IndividualReportPointsDescriptionFilterText(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, default=None, null=True, blank=True)
    filter = models.ForeignKey(IndividualReportPointsDescriptionFilter, on_delete=models.CASCADE, default=None, blank=True, null=True)
    text = models.TextField(default=None, blank=True, verbose_name='Текст описания', null=True)

    def __str__(self):
        return f'[{timezone.localtime(self.created_at).strftime("%d.%m.%Y %H:%M:%S")}] : {self.id}. {self.filter.name}'

    class Meta:
        verbose_name_plural = 'Фильтры описания баллов: Тексты описания (личные отчеты)'
        verbose_name = 'Фильтр описания баллов: Текст описания (личные отчеты)'


class IndividualReportPointsDescriptionFilterTextRecommendations(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, default=None, null=True, blank=True)
    filter_text = models.ForeignKey(IndividualReportPointsDescriptionFilterText, on_delete=models.CASCADE, default=None, blank=True, null=True)
    text = models.TextField(default=None, blank=True, verbose_name='Текст рекомендации', null=True)

    def __str__(self):
        return f'[{timezone.localtime(self.created_at).strftime("%d.%m.%Y %H:%M:%S")}] : {self.id} {self.filter_text.filter.name}'

    class Meta:
        verbose_name_plural = 'Фильтры описания баллов: Тексты рекомендаций (личные отчеты)'
        verbose_name = 'Фильтр описания баллов: Текст рекомендации (личные отчеты)'


class IndividualReportContradictionFilter(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, default=None, null=True, blank=True)
    name = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f'[{timezone.localtime(self.created_at).strftime("%d.%m.%Y %H:%M:%S")}] : {self.id}. {self.name}'

    class Meta:
        verbose_name_plural = 'Противоречия в шкалах (личные отчеты)'
        verbose_name = 'Противоречие в шкалах (личные отчеты)'


class IndividualReportContradictionFilterCategory(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, default=None, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, default=None, blank=True, null=True)
    filter = models.ForeignKey(IndividualReportContradictionFilter, on_delete=models.CASCADE, default=None, blank=True, null=True)
    points_from = models.IntegerField(null=False, default=0)
    points_to = models.IntegerField(null=False, default=0)

    def __str__(self):
        return f'[{timezone.localtime(self.created_at).strftime("%d.%m.%Y %H:%M:%S")}] : {self.id}. {self.filter.name}'

    class Meta:
        verbose_name_plural = 'Противоречия в шкалах: Категории (шкалы) (личные отчеты)'
        verbose_name = 'Противоречия в шкалах : Категория (шкалы) (личные отчеты)'


class PotentialMatrix(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, default=None, null=True, blank=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    code = models.CharField(max_length=200, blank=True, null=True)
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, default=None, null=True, blank=True)

    def __str__(self):
        return f'[{timezone.localtime(self.created_at).strftime("%d.%m.%Y %H:%M:%S")}] : {self.id}. {self.name}'

    class Meta:
        verbose_name_plural = 'Матрицы потенциала (PotentialMatrix)'
        verbose_name = 'Матрица потенциала (PotentialMatrix)'


class PotentialMatrixCategory(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, default=None, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, default=None, blank=True, null=True)
    matrix = models.ForeignKey(PotentialMatrix, on_delete=models.CASCADE, default=None, blank=True, null=True)
    points_from = models.IntegerField(null=False, default=0)
    points_to = models.IntegerField(null=False, default=0)

    def __str__(self):
        return f'[{timezone.localtime(self.created_at).strftime("%d.%m.%Y %H:%M:%S")}] : {self.id}. {self.matrix.name}'

    class Meta:
        verbose_name_plural = 'Матрицы потенциала: Категории (шкалы) (PotentialMatrixCategory)'
        verbose_name = 'Матрица потенциала: Категории (шкалы) (PotentialMatrixCategory)'


class TrafficLightReportFilter(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, default=None, null=True, blank=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    points_from_red = models.IntegerField(null=False, default=0)
    points_to_red = models.IntegerField(null=False, default=0)
    circle_diagram_description_red = models.TextField(default=None, blank=True, null=True)
    points_from_yellow = models.IntegerField(null=False, default=0)
    points_to_yellow = models.IntegerField(null=False, default=0)
    circle_diagram_description_yellow = models.TextField(default=None, blank=True, null=True)
    points_from_green = models.IntegerField(null=False, default=0)
    points_to_green = models.IntegerField(null=False, default=0)
    circle_diagram_description_green = models.TextField(default=None, blank=True, null=True)
    direction = models.CharField(max_length=30, blank=True, null=True)
    position = models.IntegerField(null=False, default=0)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, default=None, blank=True, null=True)
    for_circle_diagram = models.BooleanField(default=False)

    def __str__(self):
        return f'[{timezone.localtime(self.created_at).strftime("%d.%m.%Y %H:%M:%S")}] : {self.id}. {self.name}'

    class Meta:
        verbose_name_plural = 'Фильтры Светофор (командные отчеты)'
        verbose_name = 'Фильтр Светофор (командные отчеты)'


class TrafficLightReportFilterCategory(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, default=None, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, default=None, blank=True, null=True)
    filter = models.ForeignKey(TrafficLightReportFilter, on_delete=models.CASCADE, default=None, blank=True, null=True)

    def __str__(self):
        return f'[{timezone.localtime(self.created_at).strftime("%d.%m.%Y %H:%M:%S")}] : {self.id}. {self.filter.name}'

    class Meta:
        verbose_name_plural = 'Категории (шкалы) фильтров Светофор (командные отчеты)'
        verbose_name = 'Категория (шкалы) фильтра Светофор (командные отчеты)'


class IntegralReportFilter(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, default=None, null=True, blank=True)
    name = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f'[{timezone.localtime(self.created_at).strftime("%d.%m.%Y %H:%M:%S")}] : {self.id}. {self.name}'

    class Meta:
        verbose_name_plural = 'Фильтры интегрального отчета'
        verbose_name = 'Фильтр интегрального отчета'


class IntegralReportFilterCategory(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, default=None, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, default=None, blank=True, null=True)
    filter = models.ForeignKey(IntegralReportFilter, on_delete=models.CASCADE, default=None, blank=True, null=True)

    def __str__(self):
        return f'[{timezone.localtime(self.created_at).strftime("%d.%m.%Y %H:%M:%S")}] : {self.id}. {self.filter.name}'

    class Meta:
        verbose_name_plural = 'Категории (шкалы) фильтров интегральных отчетов'
        verbose_name = 'Категория (шкалы) фильтра интегрального отчета'


class CommonBooleanSettings(models.Model):
    value = models.BooleanField(default=False)
    name = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name_plural = 'Булевые настройки'
        verbose_name = 'Булевая настройка'


class ProcessingRuns(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    run_by = models.ForeignKey(User, on_delete=models.SET_NULL, default=None, null=True, blank=True)
    button_id = models.CharField(max_length=200, blank=True, null=True)
    name = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f'[{timezone.localtime(self.created_at).strftime("%d.%m.%Y %H:%M:%S")}] : {self.id}. {self.button_id} - ${self.name}'

    class Meta:
        verbose_name_plural = 'Запуск обработок (ProcessingRuns)'
        verbose_name = 'Запуск обработки (ProcessingRuns)'

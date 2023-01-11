import os.path

from django.db import models
from django.contrib.auth.models import User
import datetime


class Section(models.Model):
    name = models.CharField(max_length=30, blank=False, null=False)
    code = models.CharField(max_length=10, blank=True, null=True, default=None)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Секции'
        verbose_name = 'Секция'


class Category(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE, default=None, blank=True, null=True, verbose_name='Секция')
    name = models.CharField(max_length=100, blank=False, null=False)
    code = models.CharField(max_length=10, blank=True, null=True, default=None)

    def __str__(self):
        # return f'категория - {self.name}'
        return f'ID. {self.id} категория - {self.name} | секция - {self.section} | code - {self.code}'

    class Meta:
        verbose_name_plural = 'Категории'
        verbose_name = 'Категория'


class PointDescription(models.Model):
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
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    created_by = models.ForeignKey(User, default=None, null=True, on_delete=models.PROTECT)
    name = models.CharField(max_length=150, blank=False, null=False)
    version = models.IntegerField(null=True, default=0)
    active = models.BooleanField(default=True, null=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Компании'
        verbose_name = 'Компания'


class Industry(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    created_by = models.ForeignKey(User, default=None, null=True, on_delete=models.PROTECT, related_name='Создано_пользователем')
    edited_at = models.DateTimeField(auto_now=True, null=True)
    edited_by = models.ForeignKey(User, default=None, null=True, on_delete=models.PROTECT, related_name='Изменено_пользователем')
    name_ru = models.CharField(max_length=100, blank=True, null=True)
    name_en = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name_ru

    class Meta:
        verbose_name_plural = 'Индустрии'
        verbose_name = 'Индустрия'


class EmployeeRole(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    created_by = models.ForeignKey(User, default=None, null=True, on_delete=models.PROTECT, related_name='Создано_пользователем_роль_сотрудника')
    edited_at = models.DateTimeField(auto_now=True, null=True)
    edited_by = models.ForeignKey(User, default=None, null=True, on_delete=models.PROTECT, related_name='Изменено_пользователем_роль_сотрудника')
    name_ru = models.CharField(max_length=100, blank=True, null=True)
    name_en = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name_ru

    class Meta:
        verbose_name_plural = 'Роли участников'
        verbose_name = 'Роль участника'


class EmployeePosition(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    created_by = models.ForeignKey(User, default=None, null=True, on_delete=models.PROTECT)
    name_ru = models.CharField(max_length=100, blank=True, null=True)
    name_en = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name_ru

    class Meta:
        verbose_name_plural = 'Должности участников'
        verbose_name = 'Должность участника'


class Employee(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, default=None, null=True, related_name='created_by_user')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, default=None, blank=True, null=True,
                             verbose_name='Пользователь', related_name='employee_user')
    name = models.CharField(max_length=100, blank=True, null=True)
    sex = models.CharField(max_length=20, blank=False, null=False)
    birth_year = models.IntegerField(blank=False, null=False)
    email = models.CharField(max_length=100, blank=True, null=False, default=None)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, default=None, blank=True, null=True, verbose_name='Компания')
    # role = models.ForeignKey(EmployeeRole, on_delete=models.CASCADE, default=None, blank=True, null=True, verbose_name='Роль участника')
    role = models.CharField(max_length=100, blank=True, null=False, default=None)
    position = models.CharField(max_length=100, blank=True, null=False, default=None)
    # position = models.ForeignKey(EmployeePosition, on_delete=models.CASCADE, default=None, blank=True, null=True, verbose_name='Позиция участника')
    industry = models.CharField(max_length=100, blank=True, null=False, default=None)
    # industry = models.ForeignKey(Industry, on_delete=models.CASCADE, default=None, blank=True, null=True, verbose_name='Индустрия')
    company_admin = models.BooleanField(default=False, null=False)
    company_admin_active = models.BooleanField(default=False, null=False)

    def __str__(self):
        if self.name:
            return f'{self.id}. {self.name} - {self.email}'
        else:
            return f'{self.id}. {self.email}'

    class Meta:
        verbose_name_plural = 'Сотрудники (employee)'
        verbose_name = 'Сотрудник (employee)'


class Study(models.Model):
    version = models.IntegerField(null=False, default=0)
    company = models.ForeignKey(Company, on_delete=models.RESTRICT, default=None, null=True)
    research_id = models.IntegerField(null=False, default=0)
    research_name = models.CharField(max_length=100, blank=True, null=True, default=None)
    name = models.CharField(max_length=100, blank=True, null=True)
    public_code = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Опросники (studies)'
        verbose_name = 'Опросники (study)'


class Participant(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True)
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

    def __str__(self):
        if self.employee:
            return f'{self.id}. {self.employee.name}'
        else:
            return f'ID - {self.id}'

    class Meta:
        verbose_name_plural = 'Участники опроса'
        verbose_name = 'Участник опроса'


class ParticipantQuestionGroups(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, default=None, null=True)
    question_group_name = models.CharField(max_length=30, blank=True, null=True, default=None)
    question_group_code = models.CharField(max_length=2, blank=True, null=True, default=None)
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, default=None, null=True, blank=True)

    def __str__(self):
        return f'Группа вопросов - {self.question_group_name} Опросник - {self.participant}'

    class Meta:
        verbose_name_plural = 'Группы вопросов для участника'
        verbose_name = 'Группа вопросов для участника'


class EmailSentToParticipant(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, default=None, null=True, blank=True)
    participant = models.ForeignKey(Participant, on_delete=models.PROTECT, default=None, null=True)
    type = models.CharField(max_length=30, blank=True, null=True, default=None)

    def __str__(self):
        return f'{self.participant.employee.name} - {self.type}'

    class Meta:
        verbose_name_plural = 'Письма отправленные'
        verbose_name = 'Письмо отправлено'


class RawToTPointsType(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name_plural = 'Типы поправок'
        verbose_name = 'Тип поправки'


class RawToTPoints(models.Model):
    type = models.ForeignKey(RawToTPointsType, on_delete=models.CASCADE, default=None, blank=True, null=True)
    raw_points = models.IntegerField(null=False, default=0)
    t_point = models.IntegerField(null=False, default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=None, blank=True, null=True)

    def __str__(self):
        return f'{self.type.name} - {self.category.name}  {self.raw_points} - {self.t_point}'

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
    study = models.ForeignKey(Study, on_delete=models.RESTRICT, default=None, null=True, blank=True)
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
    category_name = models.CharField(max_length=50, blank=True, null=True, default=None)
    category_code = models.CharField(max_length=5, blank=True, null=True, default=None)
    points = models.IntegerField(null=False, default=0)

    def __str__(self):
        return f'{self.report.participant.employee.name} - {self.report.participant.employee.company.name} - {self.section_name} - {self.category_name} - {self.points}'

    class Meta:
        verbose_name_plural = 'Данные индивидуальных отчетов'
        verbose_name = 'Данные индивидуальных отчетов'


class ReportGroup(models.Model):
    added = models.DateTimeField(auto_now_add=True, null=True)
    file = models.FileField(upload_to='media/reportsPDF/', default=None)
    lang = models.CharField(max_length=2, blank=True, null=True, default='ru')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, default=None, blank=True, null=True, verbose_name='Проект групповой отчет')
    comments = models.TextField(default=None, blank=True, null=True, verbose_name='Комментарии групповой отчет')

    def __str__(self):
        return f'{self.company} - {self.file.name}'

    class Meta:
        verbose_name_plural = 'Групповые отчеты'
        verbose_name = 'Групповые отчеты'


class ReportGroupSquare(models.Model):
    added = models.DateTimeField(auto_now_add=True, null=True)
    report_group = models.ForeignKey(ReportGroup, on_delete=models.CASCADE, default=None, blank=True, null=True, verbose_name='Отчет групповой')
    square_name = models.CharField(max_length=30, blank=False, null=False, verbose_name='Квадрат')
    report = models.ForeignKey(Report, on_delete=models.CASCADE, default=None, blank=True, null=True, verbose_name='Отчет индивидуальный для группового')

    def __str__(self):
        return f'{self.report.participant.employee.name} - {self.square_name}'

    class Meta:
        verbose_name_plural = 'Данные по квадратам групповых отчетов'
        verbose_name = 'Данные по квадратам групповых отчетов'



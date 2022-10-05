from django.db import models


class Participant(models.Model):
    fio = models.CharField(max_length=100, blank=False, null=False)
    sex = models.CharField(max_length=20, blank=False, null=False)
    birth_year = models.IntegerField(blank=False, null=False)
    email = models.CharField(max_length=100, blank=True, null=False, default=None)

    def __str__(self):
        return self.fio


class Report(models.Model):
    code = models.CharField(max_length=30, blank=False, null=False)
    lie_points = models.IntegerField(null=False, default=0)
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, default=None, blank=True, null=True, verbose_name='Участник')
    file = models.FileField(upload_to='media/reportsPDF/', default=None)
    lang = models.CharField(max_length=2, blank=True, null=True, default=None)

    def __str__(self):
        return f'{self.participant.fio} - {self.file.url}'


class Section(models.Model):
    name = models.CharField(max_length=30, blank=False, null=False)

    def __str__(self):
        return self.name


class Category(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE, default=None, blank=True, null=True, verbose_name='Секция')
    name = models.CharField(max_length=100, blank=False, null=False)

    def __str__(self):
        # return f'категория - {self.name}'
        return f'ID. {self.id} категория - {self.name} | секция - {self.section}'


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

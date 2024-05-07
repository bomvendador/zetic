from django.db import models

from django.contrib.auth.models import User


class UserRole(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Роли пользователей'
        verbose_name = 'Роль пользователя'


class UserProfile(models.Model):
    added = models.DateTimeField(auto_now_add=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, default=None, blank=True, null=True, related_name='создано_пользователь')
    user = models.ForeignKey(User, on_delete=models.PROTECT, default=None, blank=True, null=True, related_name='Пользователь')
    role = models.ForeignKey(UserRole, on_delete=models.PROTECT, default=None, blank=True, null=True, verbose_name='Роль')
    fio = models.CharField(max_length=100, blank=False, null=False, default='ФИО')
    tel = models.CharField(max_length=20, blank=True, null=True, default='Телефон')
    active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.user.username} - {self.role.name}'

    class Meta:
        verbose_name_plural = 'Профили пользователей'
        verbose_name = 'Профиль пользователя'



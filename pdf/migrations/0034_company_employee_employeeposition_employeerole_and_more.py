# Generated by Django 4.1.1 on 2022-12-09 09:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pdf', '0033_alter_category_options_alter_participant_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('name', models.CharField(max_length=150)),
                ('version', models.IntegerField(default=0, null=True)),
                ('created_by', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Компания',
                'verbose_name_plural': 'Компании',
            },
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('fio', models.CharField(blank=True, max_length=100, null=True)),
                ('sex', models.CharField(max_length=20)),
                ('birth_year', models.IntegerField()),
                ('email', models.CharField(blank=True, default=None, max_length=100)),
                ('company', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='pdf.company', verbose_name='Проект')),
                ('created_by', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Участник (employee)',
                'verbose_name_plural': 'Участники (employee)',
            },
        ),
        migrations.CreateModel(
            name='EmployeePosition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('name_ru', models.CharField(blank=True, max_length=100, null=True)),
                ('name_eng', models.CharField(blank=True, max_length=100, null=True)),
                ('created_by', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Позиция участника',
                'verbose_name_plural': 'Позиции участников',
            },
        ),
        migrations.CreateModel(
            name='EmployeeRole',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('name_ru', models.CharField(blank=True, max_length=100, null=True)),
                ('created_by', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Роль участника',
                'verbose_name_plural': 'Роли участников',
            },
        ),
        migrations.CreateModel(
            name='Industry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('name_ru', models.CharField(blank=True, max_length=100, null=True)),
                ('name_eng', models.CharField(blank=True, max_length=100, null=True)),
                ('created_by', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Индустрия',
                'verbose_name_plural': 'Индустрии',
            },
        ),
        migrations.RenameField(
            model_name='participant',
            old_name='added',
            new_name='created_at',
        ),
        migrations.RemoveField(
            model_name='participant',
            name='project',
        ),
        migrations.RemoveField(
            model_name='reportgroup',
            name='project',
        ),
        migrations.AddField(
            model_name='participant',
            name='completed_at',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='participant',
            name='created_by',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='participant',
            name='finished_at',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='participant',
            name='started_at',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='participant',
            name='tos_accepted',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='participant',
            name='fio',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.DeleteModel(
            name='Project',
        ),
        migrations.AddField(
            model_name='employee',
            name='industry',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='pdf.industry', verbose_name='Индустрия'),
        ),
        migrations.AddField(
            model_name='employee',
            name='position',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='pdf.employeeposition', verbose_name='Позиция участника'),
        ),
        migrations.AddField(
            model_name='employee',
            name='role',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='pdf.employeerole', verbose_name='Роль участника'),
        ),
        migrations.AddField(
            model_name='participant',
            name='company',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='pdf.company', verbose_name='Компания'),
        ),
        migrations.AddField(
            model_name='participant',
            name='employee',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='pdf.employee', verbose_name='Employee'),
        ),
        migrations.AddField(
            model_name='reportgroup',
            name='company',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='pdf.company', verbose_name='Проект групповой отчет'),
        ),
    ]

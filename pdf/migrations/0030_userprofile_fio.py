# Generated by Django 4.1.1 on 2022-10-29 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pdf', '0029_userrole_alter_reportgroupsquare_square_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='fio',
            field=models.CharField(default='ФИО', max_length=100),
        ),
    ]
# Generated by Django 4.1.1 on 2022-09-15 11:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pdf', '0007_alter_participant_birth_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='participant',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='pdf.participant', verbose_name='Участник'),
        ),
    ]

# Generated by Django 4.1.1 on 2022-10-04 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pdf', '0018_alter_report_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='file',
            field=models.FileField(default=None, upload_to='reportsPDF/'),
        ),
    ]
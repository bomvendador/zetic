# Generated by Django 4.1.1 on 2022-10-04 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pdf', '0020_alter_report_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='file',
            field=models.FileField(default=None, upload_to='media/reportsPDF/'),
        ),
    ]
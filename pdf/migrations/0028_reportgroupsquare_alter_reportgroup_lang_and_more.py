# Generated by Django 4.1.1 on 2022-10-28 17:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pdf', '0027_reportgroup_reportgroupsquares'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReportGroupSquare',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added', models.DateTimeField(auto_now_add=True, null=True)),
                ('square_name', models.CharField(max_length=30)),
                ('report', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='pdf.report', verbose_name='Отчет индивидуальный для группового')),
            ],
        ),
        migrations.AlterField(
            model_name='reportgroup',
            name='lang',
            field=models.CharField(blank=True, default='ru', max_length=2, null=True),
        ),
        migrations.DeleteModel(
            name='ReportGroupSquares',
        ),
        migrations.AddField(
            model_name='reportgroupsquare',
            name='report_group',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='pdf.reportgroup', verbose_name='Отчет групповой'),
        ),
    ]
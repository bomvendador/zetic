from django.contrib import admin
from pdf.models import Participant, Report, Category, Section, PointDescription

# Register your models here.


admin.site.register(Participant)
admin.site.register(Report)
admin.site.register(Category)
admin.site.register(Section)
admin.site.register(PointDescription)

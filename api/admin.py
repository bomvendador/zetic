from django.contrib import admin
from pdf.models import Participant, Report, Category, Section, PointDescription, Company, ReportData, ReportGroup, \
    ReportGroupSquare, Industry, EmployeeRole, EmployeePosition, Employee, Study, StudyQuestionGroups, EmailSentToParticipant
from login.models import UserRole, UserProfile

# Register your models here.


admin.site.register(Participant)
admin.site.register(Report)
admin.site.register(Category)
admin.site.register(Section)
admin.site.register(PointDescription)
admin.site.register(Company)
admin.site.register(ReportData)
admin.site.register(ReportGroup)
admin.site.register(ReportGroupSquare)
admin.site.register(UserRole)
admin.site.register(UserProfile)
admin.site.register(Industry)
admin.site.register(EmployeePosition)
admin.site.register(EmployeeRole)
admin.site.register(Employee)
admin.site.register(Study)
admin.site.register(StudyQuestionGroups)
admin.site.register(EmailSentToParticipant)

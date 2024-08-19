from django.contrib import admin
from pdf.models import Participant, Report, Category, Section, PointDescription, Company, ReportData, ReportGroup, \
    ReportGroupSquare, Industry, EmployeeRole, EmployeePosition, Employee, Study, EmailSentToParticipant, \
    RawToTPointsType, RawToTPoints, EmployeeGender, ResearchTemplate, ResearchTemplateSections, CategoryQuestions, QuestionAnswers, \
    AgeGenderGroup, Questionnaire, QuestionnaireQuestionAnswers, MatrixFilter, MatrixFilterCategory, MatrixFilterInclusiveEmployeePosition, \
    MatrixFilterParticipantNotDistributed, MatrixFilterParticipantNotDistributedEmployeePosition, ReportDataByCategories, \
    Project, ProjectStudy, ProjectParticipants, TrafficLightReportFilter, TrafficLightReportFilterCategory
from login.models import UserRole, UserProfile


# Register your models here.
class ReportAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at',)


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
# admin.site.register(ParticipantQuestionGroups)
admin.site.register(EmailSentToParticipant, ReportAdmin)
admin.site.register(RawToTPointsType)
admin.site.register(RawToTPoints)
admin.site.register(EmployeeGender)
admin.site.register(ResearchTemplate)
admin.site.register(ResearchTemplateSections)
admin.site.register(CategoryQuestions)
admin.site.register(QuestionAnswers)
admin.site.register(AgeGenderGroup)
admin.site.register(Questionnaire)
admin.site.register(QuestionnaireQuestionAnswers)
admin.site.register(MatrixFilter)
admin.site.register(MatrixFilterCategory)
admin.site.register(MatrixFilterInclusiveEmployeePosition)
admin.site.register(MatrixFilterParticipantNotDistributed)
admin.site.register(MatrixFilterParticipantNotDistributedEmployeePosition)
admin.site.register(ReportDataByCategories)
admin.site.register(Project)
admin.site.register(ProjectStudy)
admin.site.register(ProjectParticipants)
admin.site.register(TrafficLightReportFilter)
admin.site.register(TrafficLightReportFilterCategory)

from django.urls import path
# import views as pdf_views
from pdf import views as pdf_views
from sendemail import tasks

urlpatterns = [
    path('fpdf', tasks.pdf_single_generator_task, name="pdf_single_generator"),
    # path('fpdf', pdf_views.pdf_single_generator, name="pdf_single_generator"),
    path('pdf_regenerate_report', pdf_views.regenerate_report, name="pdf_regenerate_report"),

]
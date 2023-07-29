from django.urls import path

# import views as pdf_views
from pdf import views as pdf_views

urlpatterns = [
    path("fpdf", pdf_views.pdf_single_generator_v1, name="pdf_single_generator"),
]

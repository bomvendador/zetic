from django.urls import path
# import views as pdf_views
from . import participant_data, questionnaire_sections

urlpatterns = [
    path('save_answers', questionnaire_sections.save_answers, name='save_answers'),
    path('save_participant_data', participant_data.save_participant_data,
         name='questionnaire_save_participant_data'),

    path('section/<int:section_id>/<str:code>', questionnaire_sections.section_view, name='section_view'),
    path('<str:code>', participant_data.get_participant_data, name='participant_data'),

]
from django.urls import path
# import views as pdf_views
from panel import views as panel_views
from pdf import views as pdf_views
from panel import company_parameter as panel_company_parameter
from panel import employee, study, sections, individual_report_file, company, mail_handler, categories, questions, \
    research_templates, companies_studies, filters, filters_matrix, migration_questionnaire_results_xls, \
    filters_individual_report_points_description, filters_integral_report, projects, \
    filters_traffic_light_report, search
from panel.common_settings import settings, notification_report_made_receivers
from panel.consultant_form import panel_consultant_form
# from panel import study
# from panel import individual_report_file
# from panel import company
# from panel import mail_handler
from sendemail import tasks



urlpatterns = [
    path('', panel_views.home, name="panel_home"),
    path('team_distribution', panel_views.team_distribution, name='team_distribution'),
    path('get_company_projects_for_group_report', panel_views.get_company_projects_for_group_report, name='get_company_projects_for_group_report'),
    path('get_company_projects_with_group_report', panel_views.get_company_projects_with_group_report, name='get_company_projects_with_group_report'),
    path('get_participants_by_project_studies', panel_views.get_participants_by_project_studies, name='get_participants_by_project_studies'),
    path('get_report_participants_data', panel_views.get_report_participants_data, name='get_report_participants_data'),
    path('download_file/<str:filename>', pdf_views.download_file, name='download_file'),
    path('logout', panel_views.panel_logout, name='logout'),
    path('users_list', panel_views.users_list, name='users_list'),
    path('user_profile/<int:user_id>', panel_views.user_profile, name='user_profile'),
    path('save_user_pwd', panel_views.save_user_pwd, name='save_user_pwd'),
    path('save_user_profile', panel_views.save_user_profile, name='save_user_profile'),
    path('add_user', panel_views.add_user, name='add_user'),
    path('save_new_user', panel_views.save_new_user, name='save_new_user'),
    path('delete_user', panel_views.delete_user, name='delete_user'),

    path('individual_reports_list', panel_views.individual_reports_list, name='individual_reports_list'),
    path('get_individual_reports_list', panel_views.get_individual_reports_list, name='get_individual_reports_list'),
    path('save_individual_report_comments', panel_views.save_individual_report_comments,
         name='save_individual_report_comments'),
    path('download_single_report/<str:filename>', pdf_views.download_single_report, name='download_single_report'),

    path('save_group_report_data', panel_views.save_group_report_data, name='save_group_report_data'),
    path('download_group_report/<str:filename>', pdf_views.download_group_report, name='download_group_report'),
    path('get_group_reports_list', panel_views.get_group_reports_list, name='get_group_reports_list'),
    path('group_reports_list', panel_views.group_reports_list, name='group_reports_list'),
    path('delete_group_report', panel_views.delete_group_report, name='delete_group_report'),
    path('save_group_report_comments', panel_views.save_group_report_comments, name='save_group_report_comments'),
    path('delete_participant_from_group_report', panel_views.delete_participant_from_group_report, name='delete_participant_from_group_report'),
    path('get_available_participants_for_group_report', panel_views.get_available_participants_for_group_report, name='get_available_participants_for_group_report'),
    path('edit_group_report_data/<int:report_id>/<int:project_id>', panel_views.edit_group_report_data, name='edit_group_report_data'),

    path('add_company', company.add_company_init, name='add_company_init'),
    path('save_new_company', company.save_new_company, name='save_new_company'),
    path('update_company', company.update_company, name='update_company'),
    path('generate_new_self_questionnaire_link', company.generate_new_self_questionnaire_link, name='generate_new_self_questionnaire_link'),
    path('companies_list', company.companies_list, name='companies_list'),
    path('company/<int:company_id>', company.edit_company, name='edit_company'),
    path('company_questionnaire/<str:code>', company.company_questionnaire, name='company_questionnaire'),
    path('appoint_company_admin', company.appoint_company_admin, name='appoint_company_admin'),
    path('create_self_questionnaire', company.create_self_questionnaire, name='create_self_questionnaire'),
    path('add_report_made_notification_receiver', company.add_report_made_notification_receiver, name='add_report_made_notification_receiver'),
    path('delete_report_made_notification_receiver', company.delete_report_made_notification_receiver, name='delete_report_made_notification_receiver'),
    path('update_company_report_options_allowed', company.update_company_report_options_allowed, name='update_company_report_options_allowed'),

    path('industries_list', panel_company_parameter.industries_list, name='industries_list'),
    path('save_new_industry', panel_company_parameter.save_new_industry, name='save_new_industry'),
    path('edit_industry', panel_company_parameter.edit_industry, name='edit_industry'),
    path('delete_industry', panel_company_parameter.delete_industry, name='delete_industry'),

    path('employees_roles_list', panel_company_parameter.employees_roles_list, name='employees_roles_list'),
    path('save_new_employee_role', panel_company_parameter.save_new_employee_role, name='save_new_employee_role'),
    path('edit_employee_role', panel_company_parameter.edit_employee_role, name='edit_employee_role'),
    path('delete_employee_role', panel_company_parameter.delete_employee_role, name='delete_employee_role'),
    path('employees_positions_list', panel_company_parameter.employees_positions_list, name='employees_positions_list'),
    path('save_new_employee_position', panel_company_parameter.save_new_employee_position, name='save_new_employee_position'),
    path('edit_employee_position', panel_company_parameter.edit_employee_position, name='edit_employee_position'),
    path('delete_employee_position', panel_company_parameter.delete_employee_position, name='delete_employee_position'),

    path('get_company_employees', employee.get_company_employees, name='get_company_employees'),
    path('add_employee', employee.add_employee, name='add_employee'),
    path('delete_employee', employee.delete_employee, name='delete_employee'),
    path('save_new_employee_xls', employee.save_new_employee_xls, name='save_new_employee_xls'),
    path('save_new_employee_html', employee.save_new_employee_html, name='save_new_employee_html'),
    path('employees_list', employee.employees_list, name='employees_list'),
    path('get_employee_data', employee.get_employee_data, name='get_employee_data'),
    path('get_company_no_admins', employee.get_company_no_admins, name='get_company_no_admins'),
    path('deactivate_company_admin', employee.deactivate_company_admin, name='deactivate_company_admin'),
    path('delete_company_admin', employee.delete_company_admin, name='delete_company_admin'),

    path('search_employees', search.search_employees, name='search_employees'),
    path('search_questionnaire_status', search.search_questionnaire_status, name='search_questionnaire_status'),
    path('search_for_employees', search.search_for_employees, name='search_for_employees'),
    path('search_for_questionnaire_status', search.search_for_questionnaire_status, name='search_for_questionnaire_status'),

    path('delete_company', company.delete_company, name='delete_company'),

    path('studies_list', study.studies_list, name='studies_list'),
    path('get_company_studies', study.get_company_studies, name='get_company_studies'),
    path('study/<str:study_id>', study.study_details, name='study_details'),
    # path('get_question_groups', study.get_question_groups, name='get_question_groups'),
    # path('save_participant_questions_groups', study.save_participant_questions_groups, name='save_participant_questions_groups'),
    path('get_employees_for_study', study.get_employees_for_study, name='get_employees_for_study'),
    path('save_study_participants', study.save_study_participants, name='save_study_participants'),
    path('save_study_name', study.save_study_name, name='save_study_name'),
    path('delete_participants_from_study', study.delete_participants_from_study, name='delete_participants_from_study'),
    path('change_questionnaire_status', study.change_questionnaire_status, name='change_questionnaire_status'),
    path('get_participants_raw_points', study.get_participants_raw_points, name='get_participants_raw_points'),
    path('save_participants_individual_report_options', study.save_participants_individual_report_options, name='save_participants_individual_report_options'),

    path('individual_report_file_index', individual_report_file.individual_report_file_index, name='individual_report_file_index'),

    path('send_invitation_email', mail_handler.send_invitation_email, name='send_invitation_email'),
    path('mass_send_invitation_email', mail_handler.mass_send_invitation_email, name='mass_send_invitation_email'),

    path('monthly_report', tasks.monthly_report, name='monthly_report'),

    path('migration', panel_views.migration, name='migration'),
    path('save_migration', panel_views.save_migration, name='save_migration'),

    path('sections_list', sections.sections_list, name='sections_list'),
    path('edit_section', sections.edit_section, name='edit_section'),
    path('delete_section', sections.delete_section, name='delete_section'),
    path('save_new_section', sections.save_new_section, name='save_new_section'),

    path('categories_list', categories.categories_list, name='categories_list'),
    path('get_categories_by_section', categories.get_categories_by_section, name='get_categories_by_section'),
    path('edit_category', categories.edit_category, name='edit_category'),
    path('delete_category', categories.delete_category, name='delete_category'),
    path('save_new_category', categories.save_new_category, name='save_new_category'),
    # path('get_company_employees', employee.get_company_employees, name='get_company_employees'),

    path('questions/<int:category_id>', questions.questions_list, name='questions_list'),
    path('add_new_question', questions.add_new_question, name='add_new_question'),
    path('get_question_data', questions.get_question_data, name='get_question_data'),
    path('delete_answer', questions.delete_answer, name='delete_answer'),
    path('delete_question', questions.delete_question, name='delete_question'),
    path('edit_question', questions.edit_question, name='edit_question'),

    path('research_templates_list', research_templates.research_templates_list, name='research_templates_list'),
    path('get_research_template_data', research_templates.get_research_template_data, name='get_research_template_data'),
    path('get_all_sections', research_templates.get_all_sections, name='get_all_sections'),
    path('add_new_research_template', research_templates.add_new_research_template, name='add_new_research_template'),
    path('add_new_research_template', research_templates.edit_research_template, name='edit_research_template'),
    path('delete_section_from_template', research_templates.delete_section_from_template, name='delete_section_from_template'),
    path('edit_research_template', research_templates.edit_research_template, name='edit_research_template'),
    path('delete_template', research_templates.delete_template, name='delete_template'),

    path('companies_studies_list', companies_studies.companies_studies_list, name='companies_studies_list'),
    path('add_study', companies_studies.add_study, name='add_study'),
    path('get_company_employees_for_new_study', companies_studies.get_company_employees, name='get_company_employees_for_new_study'),
    path('add_new_study', companies_studies.add_new_study, name='add_new_study'),
    path('get_company_options_allowed', companies_studies.get_company_options_allowed, name='get_company_options_allowed'),
    # path('edit_company_study/<int:study_id>', companies_studies.edit_company_study, name='edit_company_study'),

    path('filters_list', filters.filters_list, name='filters_list'),
    path('add_filter', filters.add_filter, name='add_filter'),
    # path('save_new_filter', filters.save_new_filter, name='save_new_filter'),
    path('save_new_filter_from_file', filters.save_new_filter_from_file, name='save_new_filter_from_file'),
    path('delete_filter', filters.delete_filter, name='delete_filter'),
    path('save_edited_filter', filters.save_edited_filter, name='save_edited_filter'),
    path('filter/<int:filter_id>', filters.edit_filter, name='edit_filter'),

    path('filters_matrix_list', filters_matrix.filters_list, name='filters_matrix_list'),
    path('add_filter_mitrix', filters_matrix.add_filter, name='add_filter_matrix'),
    path('add_filter_matrix_participant_not_distributed', filters_matrix.add_filter_participant_not_distributed, name='add_filter_matrix_participant_not_distributed'),
    path('save_new_matrix_filter', filters_matrix.save_new_matrix_filter, name='save_new_matrix_filter'),
    path('save_new_matrix_filter_for_participants_not_distributed', filters_matrix.save_new_matrix_filter_for_participants_not_distributed, name='save_new_matrix_filter_for_participants_not_distributed'),
    path('save_edited_matrix_filter', filters_matrix.save_edited_matrix_filter, name='save_edited_matrix_filter'),
    path('save_edited_matrix_filter_for_participants_not_distributed', filters_matrix.save_edited_matrix_filter_for_participants_not_distributed, name='save_edited_matrix_filter_for_participants_not_distributed'),
    path('delete_matrix_filter', filters_matrix.delete_matrix_filter, name='delete_matrix_filter'),
    # path('get_available_squares', filters_matrix.get_available_squares, name='get_available_squares'),
    path('matrix_filter/<int:filter_id>', filters_matrix.edit_matrix_filter, name='edit_matrix_filter'),
    path('edit_matrix_filter_for_participants_not_distributed/<int:filter_id>', filters_matrix.edit_matrix_filter_for_participants_not_distributed, name='edit_matrix_filter_for_participants_not_distributed'),
    path('delete_matrix_filter_for_participants_not_distributed', filters_matrix.delete_matrix_filter_for_participants_not_distributed, name='delete_matrix_filter_for_participants_not_distributed'),

    path('individual_report_points_description_filters_list', filters_individual_report_points_description.individual_report_points_description_filters_list, name='individual_report_points_description_filters_list'),
    path('add_individual_report_points_description_filter', filters_individual_report_points_description.add_filter, name='add_individual_report_points_description_filter'),
    path('save_new_individual_report_points_description_filter', filters_individual_report_points_description.save_new_individual_report_points_description_filter, name='save_new_individual_report_points_description_filter'),
    path('save_edited_individual_report_points_description_filter', filters_individual_report_points_description.save_edited_individual_report_points_description_filter, name='save_edited_individual_report_points_description_filter'),
    path('individual_report_points_description_filter/<int:filter_id>', filters_individual_report_points_description.edit_individual_report_points_description_filter, name='individual_report_points_description_filter'),

    path('integral_report_filters_list', filters_integral_report.integral_report_filters_list, name='integral_report_filters_list'),
    path('add_integral_report_filter', filters_integral_report.add_filter, name='add_integral_report_filter'),
    path('save_new_integral_report_filter', filters_integral_report.save_new_integral_report_filter, name='save_new_integral_report_filter'),
    path('save_edited_integral_report_filter', filters_integral_report.save_edited_integral_report_filter, name='save_edited_integral_report_filter'),
    path('delete_integral_report_filter', filters_integral_report.delete_integral_report_filter, name='delete_integral_report_filter'),
    path('integral_report_filter/<int:filter_id>', filters_integral_report.edit_integral_report_filter, name='edit_integral_report_filter'),

    path('migration_questionnaire_results_xls_home', migration_questionnaire_results_xls.migration_home, name='migration_questionnaire_results_xls_home'),
    path('save_report_data_from_xls', migration_questionnaire_results_xls.save_report_data_from_xls, name='save_report_data_from_xls'),

    path('settings_main', settings.settings_main, name='settings_main'),
    path('save_boolean_setting', settings.save_boolean_setting, name='save_boolean_setting'),
    path('notification_report_made_receivers_home', notification_report_made_receivers.notification_report_made_receivers_home, name='notification_report_made_receivers_home'),
    path('add_common_report_made_notification_receiver', notification_report_made_receivers.add_common_report_made_notification_receiver, name='add_common_report_made_notification_receiver'),
    path('delete_common_report_made_notification_receiver', notification_report_made_receivers.delete_common_report_made_notification_receiver, name='delete_common_report_made_notification_receiver'),

    path('projects_list', projects.projects_list, name='projects_list'),
    path('get_company_projects', projects.get_company_projects, name='get_company_projects'),
    path('get_company_studies_for_project', projects.get_company_studies, name='get_company_studies_for_project'),
    path('add_new_project', projects.add_new_project, name='add_new_project'),
    path('save_new_project', projects.save_new_project, name='save_new_project'),
    path('save_edited_project', projects.save_edited_project, name='save_edited_project'),
    path('edit_project/<int:project_id>', projects.edit_project, name='edit_project'),

    path('traffic_light_report_filters_list', filters_traffic_light_report.traffic_light_report_filters_list, name='traffic_light_report_filters_list'),
    path('add_traffic_light_report_filter', filters_traffic_light_report.add_filter, name='add_traffic_light_report_filter'),
    path('add_traffic_light_report_filter_to_project/<int:project_id>',
         filters_traffic_light_report.add_traffic_light_report_filter_to_project, name='add_traffic_light_report_filter_to_project'),

    path('save_new_traffic_light_report_filter', filters_traffic_light_report.save_new_traffic_light_report_filter, name='save_new_traffic_light_report_filter'),
    path('save_edited_traffic_light_report_filter', filters_traffic_light_report.save_edited_traffic_light_report_filter, name='save_edited_traffic_light_report_filter'),
    path('edit_traffic_light_report_filter/<int:filter_id>', filters_traffic_light_report.edit_traffic_light_report_filter, name='edit_traffic_light_report_filter'),
    path('delete_traffic_light_report_filter', filters_traffic_light_report.delete_traffic_light_report_filter,
         name='delete_traffic_light_report_filter'),

    path('add_consultant_form', panel_consultant_form.add_consultant_form, name='add_consultant_form'),
    path('get_available_consultants', company.get_available_consultants, name='get_available_consultants'),
    path('add_consultant_for_company', company.add_consultant_for_company, name='add_consultant_for_company'),
    path('delete_consultant_fromm_company', company.delete_consultant_fromm_company, name='delete_consultant_fromm_company'),
    path('delete_consultant_study_from_company', company.delete_consultant_study_from_company, name='delete_consultant_study_from_company'),
    path('get_available_consultant_company_studies', company.get_available_consultant_company_studies, name='get_available_consultant_company_studies'),
    path('add_consultant_study_for_company', company.add_consultant_study_for_company, name='add_consultant_study_for_company'),
    path('get_consultant_company_studies', panel_consultant_form.get_consultant_company_studies, name='get_consultant_company_studies'),
    path('get_study_participants', panel_consultant_form.get_study_participants, name='get_study_participants'),
    path('save_consultant_form', panel_consultant_form.save_consultant_form, name='save_consultant_form'),
    path('edit_consultant_form_list', panel_consultant_form.edit_consultant_form_list, name='edit_consultant_form_list'),
    path('get_consultant_forms', panel_consultant_form.get_consultant_forms, name='get_consultant_forms'),
    path('delete_consultant_form', panel_consultant_form.delete_consultant_form, name='delete_consultant_form'),
    path('send_report_to_participant_with_consultant_text', panel_consultant_form.send_report_to_participant_with_consultant_text, name='send_report_to_participant_with_consultant_text'),
    path('download_consultant_forms', panel_consultant_form.download_consultant_forms, name='download_consultant_forms'),
    path('add_consultant_form_template/<int:participant_id>', panel_consultant_form.add_consultant_form_template, name='add_consultant_form_template'),
    path('edit_consultant_form/<int:form_id>', panel_consultant_form.edit_consultant_form, name='edit_consultant_form'),

]


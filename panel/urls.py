from django.urls import path
# import views as pdf_views
from panel import views as panel_views
from pdf import views as pdf_views
from panel import company_parameter as panel_company_parameter
from panel import employee
from panel import study
from panel import individual_report_file
from panel import company
from panel import mail_handler
from sendemail import tasks

urlpatterns = [
    path('', panel_views.home, name="panel_home"),
    path('team_distribution', panel_views.team_distribution, name='team_distribution'),
    path('get_project_participants', panel_views.get_company_participants, name='get_project_participants'),
    path('get_report_participants_data', panel_views.get_report_participants_data, name='get_report_participants_data'),
    path('save_group_report_data', panel_views.save_group_report_data, name='save_group_report_data'),
    path('download_single_report/<str:filename>', pdf_views.download_single_report, name='download_single_report'),
    path('send_individual_report', panel_views.send_individual_report, name='send_individual_report'),
    path('download_group_report/<str:filename>', pdf_views.download_group_report, name='download_group_report'),
    path('download_file/<str:filename>', pdf_views.download_file, name='download_file'),
    path('logout', panel_views.panel_logout, name='logout'),
    path('get_group_reports_list', panel_views.get_group_reports_list, name='get_group_reports_list'),
    path('group_reports_list', panel_views.group_reports_list, name='group_reports_list'),
    path('individual_reports_list', panel_views.individual_reports_list, name='individual_reports_list'),
    path('get_individual_reports_list', panel_views.get_individual_reports_list, name='get_individual_reports_list'),
    path('save_individual_report_comments', panel_views.save_individual_report_comments, name='save_individual_report_comments'),
    path('save_group_report_comments', panel_views.save_group_report_comments, name='save_group_report_comments'),
    path('users_list', panel_views.users_list, name='users_list'),
    path('user_profile/<int:user_id>', panel_views.user_profile, name='user_profile'),
    path('save_user_pwd', panel_views.save_user_pwd, name='save_user_pwd'),
    path('save_user_profile', panel_views.save_user_profile, name='save_user_profile'),
    path('add_user', panel_views.add_user, name='add_user'),
    path('save_new_user', panel_views.save_new_user, name='save_new_user'),
    path('delete_user', panel_views.delete_user, name='delete_user'),
    path('delete_group_report', panel_views.delete_group_report, name='delete_group_report'),

    path('add_company', company.add_company_init, name='add_company_init'),
    path('save_new_company', company.save_new_company, name='save_new_company'),
    path('update_company', company.update_company, name='update_company'),
    path('companies_list', company.companies_list, name='companies_list'),
    path('company/<int:company_id>', company.edit_company, name='edit_company'),
    path('appoint_company_admin', company.appoint_company_admin, name='appoint_company_admin'),

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
    path('delete_company', company.delete_company, name='delete_company'),

    path('studies_list', study.studies_list, name='studies_list'),
    path('get_company_studies', study.get_company_studies, name='get_company_studies'),
    path('study/<str:study_public_code>', study.study_details, name='study_details'),
    # path('get_question_groups', study.get_question_groups, name='get_question_groups'),
    path('save_participant_questions_groups', study.save_participant_questions_groups, name='save_participant_questions_groups'),
    path('get_employees_for_study', study.get_employees_for_study, name='get_employees_for_study'),
    path('save_study_participants', study.save_study_participants, name='save_study_participants'),

    path('individual_report_file_index', individual_report_file.individual_report_file_index, name='individual_report_file_index'),

    path('create_questionnaire', study.create_questionnaire, name='create_questionnaire'),
    path('send_invitation_email', mail_handler.send_invitation_email, name='send_invitation_email'),

    path('monthly_report', tasks.monthly_report, name='monthly_report'),

    path('migration', panel_views.migration, name='migration'),
    path('save_migration', panel_views.save_migration, name='save_migration'),

    # path('get_company_employees', employee.get_company_employees, name='get_company_employees'),


]

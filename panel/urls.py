from django.urls import path
# import views as pdf_views
from panel import views as panel_views
from pdf import views as pdf_views
from panel import company_parameter as panel_company_parameter
from panel import employee
from panel import study
from panel import individual_report_file

urlpatterns = [
    path('', panel_views.home, name="panel_home"),
    path('team_distribution', panel_views.team_distribution, name='team_distribution'),
    path('get_project_participants', panel_views.get_company_participants, name='get_project_participants'),
    path('get_report_participants_data', panel_views.get_report_participants_data, name='get_report_participants_data'),
    path('save_group_report_data', panel_views.save_group_report_data, name='save_group_report_data'),
    path('download_single_report/<str:filename>', pdf_views.download_single_report, name='download_single_report'),
    path('download_group_report/<str:filename>', pdf_views.download_group_report, name='download_group_report'),
    path('logout', panel_views.panel_logout, name='logout'),
    path('get_group_reports_list', panel_views.get_group_reports_list, name='get_group_reports_list'),
    path('group_reports_list', panel_views.group_reports_list, name='group_reports_list'),
    path('individual_reports_list', panel_views.individual_reports_list, name='individual_reports_list'),
    path('get_individual_reports_list', panel_views.get_individual_reports_list, name='get_individual_reports_list'),
    path('users_list', panel_views.users_list, name='users_list'),
    path('user_profile/<int:user_id>', panel_views.user_profile, name='user_profile'),
    path('save_user_pwd', panel_views.save_user_pwd, name='save_user_pwd'),
    path('save_user_profile', panel_views.save_user_profile, name='save_user_profile'),
    path('add_user', panel_views.add_user, name='add_user'),
    path('save_new_user', panel_views.save_new_user, name='save_new_user'),
    path('delete_user', panel_views.delete_user, name='delete_user'),
    path('delete_group_report', panel_views.delete_group_report, name='delete_group_report'),
    path('add_company', panel_views.add_company_init, name='add_company_init'),
    path('save_new_company', panel_views.save_new_company, name='save_new_company'),
    path('companies_list', panel_views.companies_list, name='companies_list'),
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
    path('company/<int:company_id>', panel_views.edit_company, name='edit_company'),
    path('get_company_employees', employee.get_company_employees, name='get_company_employees'),
    path('add_employee', employee.add_employee, name='add_employee'),
    path('save_new_employee_xls', employee.save_new_employee_xls, name='save_new_employee_xls'),
    path('save_new_employee_html', employee.save_new_employee_html, name='save_new_employee_html'),
    path('employees_list', employee.employees_list, name='employees_list'),
    path('get_employee_data', employee.get_employee_data, name='get_employee_data'),
    path('studies_list', study.studies_list, name='studies_list'),
    path('get_company_studies', study.get_company_studies, name='get_company_studies'),
    path('study/<int:study_id>', study.study_details, name='study_details'),
    path('get_question_groups', study.get_question_groups, name='get_question_groups'),
    path('save_study_questions_groups', study.save_study_questions_groups, name='save_study_questions_groups'),
    path('get_employees_for_study', study.get_employees_for_study, name='get_employees_for_study'),
    path('save_study_participants', study.save_study_participants, name='save_study_participants'),
    path('individual_report_file_index', individual_report_file.individual_report_file_index, name='individual_report_file_index'),

    # path('get_company_employees', employee.get_company_employees, name='get_company_employees'),


]
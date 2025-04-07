// console.log(`${window.location.protocol} ${window.location.host}`)

if (tech_works === 'True' && cur_user_role_name !== 'Суперадмин') {
    window.location.href = url_tech_works
}

$('.menu_item').each(function () {
    $(this).removeClass('active')
})
let token = csrf_token;


$('.menu_item').on('click', function () {
    let menuID = $(this).attr('id');
    show_progressbar_loader()
    switch (menuID) {
        case'menu_distribution':
            window.location.href = url_team_distribution;
            break;
        case'menu_dashboard':
            window.location.href = url_panel_home;
            break;
        case'menu_group_reports_list':
            window.location.href = url_group_reports_list;
            break;
        case'menu_individual_reports_list':
            window.location.href = url_individual_reports_list;
            break;
        case'menu_users_list':
            window.location.href = url_users_list;
            break;
        case'menu_employee_functions_list':
            window.location.href = url_employees_roles_list;
            break;
        case'menu_users_add':
            window.location.href = url_add_user;
            break;
        case'menu_company_add':
            window.location.href = url_add_company;
            break;
        case'menu_companies_list':
            window.location.href = url_companies_list;
            break;
        case'menu_industries_list':
            window.location.href = url_industries_list;
            break;
        case'menu_employees_roles_list':
            window.location.href = url_employees_roles_list;
            break;
        case'menu_employees_positions_list':
            window.location.href = url_employees_positions_list;
            break;
        case'menu_employee_add':
            window.location.href = url_add_employee;
            break;
        case'menu_employees_list':
            window.location.href = url_employees_list;
            break;
        case'menu_search':
            window.location.href = url_search_employees;
            break;
        case'menu_study_list':
            window.location.href = url_studies_list;
            break;
        case'menu_individual_reports_add':
            window.location.href = url_individual_report_file_index;
            break;
        case'menu_monthly_report':
            window.location.href = url_monthly_report;
            break;
        case'menu_migration':
            window.location.href = url_migration;
            break;
        case'menu_sections_list':
            window.location.href = url_sections_list;
            break;
        case'menu_categories_list':
            window.location.href = url_categories_list;
            break;
        case'menu_research_templates_list':
            window.location.href = url_research_templates_list;
            break;
        case'menu_companies_studies_list':
            window.location.href = url_companies_studies_list;
            break;
        case'menu_filters_list':
            window.location.href = url_filters_list;
            break;
        // case'menu_matrix_filters_list':
        //     window.location.href = url_filters_matrix_list;
        //     break;
        case'menu_add_questionnaire_results_xls':
            window.location.href = url_migration_questionnaire_results_xls_home;
            break;
        // case'menu_individual_report_points_description_filters_list':
        //     window.location.href = url_individual_report_points_description_filters_list;
        //     break;
        // case'menu_integral_report_filters_list':
        //     window.location.href = url_integral_report_filters_list;
        //     break;
        case'menu_settings':
            window.location.href = url_settings_main;
            break;
        case'menu_projects_list':
            window.location.href = url_projects_list;
            break;
        case'menu_project_add':
            window.location.href = url_add_new_project;
            break;
        case'menu_consultant_form_add':
            window.location.href = url_add_consultant_form;
            break;
        case'menu_consultant_form_list':
            window.location.href = url_edit_consultant_form_list;
            break;
        case'menu_processing':
            window.location.href = url_processing_main;
            break;
        case'menu_statistics_report_1':
            window.location.href = url_statistics_report_1;
            break;
        default:
            break;
    }
})

$(".list-table").DataTable({
    "searching": true,
    "destroy": true,
    "paging": false,
    "language": {
        "url": "//cdn.datatables.net/plug-ins/9dcbecd42ad/i18n/Russian.json"
    },
    "initComplete": function () {

    },
})

$('#logout').on('click', function () {

    $.ajax({
        headers: {"X-CSRFToken": token},
        url: url_logout,
        type: 'POST',

        data: '',
        processData: false,
        contentType: false,
        error: function (data) {
            toastr.error('Ошибка', data)
            console.log(data)
        },
        success: function (data) {
            // location.reload()
            window.location.href = url_login_home;

        }
    });

})

function btn_spinner(element) {
    $(element).html('<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true" style="width: 25px;height: 25px"></span>').addClass('disabled')
}

function btn_text(element, text) {
    $(element).html(text).removeClass('disabled')
}

function process_table(element) {
    $(element).DataTable().destroy()
    let table = $(element).DataTable({
        // fixedHeader: true,
        "searching": true,
        "destroy": true,
        "paging": false,
        "language": {
            "url": "//cdn.datatables.net/plug-ins/9dcbecd42ad/i18n/Russian.json"
        },
        "initComplete": function () {

        },
    })
    $(element).find('td').css('white-space', 'initial')
    return table
}

function process_table_clear(element) {
    $(element).DataTable({
        "searching": true,
        "destroy": true,
        "paging": false,
        "language": {
            "url": "//cdn.datatables.net/plug-ins/9dcbecd42ad/i18n/Russian.json"
        },
        "initComplete": function () {

        },
    })
}


function process_table_clear_with_excel_btn(element, title) {
    $(element).DataTable({
        dom: 'Bfrtip',
        buttons: [
            {
                extend: 'excelHtml5',
                text: '<i class="fe fe-download"></i>  Excel',
                className: 'btn-export',
                title: title,
                download: 'open',
            },

        ],
        "searching": true,
        "destroy": true,
        "paging": false,
        "language": {
            "url": "//cdn.datatables.net/plug-ins/9dcbecd42ad/i18n/Russian.json"
        },
        "initComplete": function () {

        },
    })
}


function expand_menu_item(item_id) {
    $(item_id).closest('.slide').addClass('is-expanded')
    $(item_id).addClass('active')
}

function show_progressbar_loader() {
    $('#content_progressbar_loader').removeClass('d-none')
}

function hide_progressbar_loader() {
    $('#content_progressbar_loader').addClass('d-none')
}

function isEmail(email) {
    let regex = /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/;
    return regex.test(email);
}

function set_checkbox_checked(el) {
    $(el).attr('checked', 'checked')
    $(el).prop('checked', true)
    $(el).val(1)
}

function set_checkbox_unchecked(el) {
    $(el).removeAttr('checked')
    $(el).prop('checked', false)
    $(el).val(0)
}

function isYear(year) {
    let regex = /^\d\d\d\d$/g
    return regex.test(year);
}

function fake_download_file(file_name) {
    let link = document.createElement('a');
    link.href = 'download_file/' + file_name;
    link.target = '_blank'
    document.body.appendChild(link);
    link.click();
}
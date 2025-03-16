expand_menu_item('#menu_statistics_report_1')

$('#statistics_reports_report_type_select_filter').on('change', function () {
    let selected_filter = $(this).val()

    if (selected_filter !== current_filter_selected) {
        switch (selected_filter) {
            case 'report_1':
                window.location.href = url_statistics_report_1;
                break;
            case 'search_employees_select':
                window.location.href = url_search_employees;
                break;
            default:
                break;

        }
    }
})


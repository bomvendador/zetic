expand_menu_item('#menu_search')

console.log(current_filter_selected)

$('#search_select_filter').on('change', function () {
    let selected_filter = $(this).val()
    if (selected_filter !== current_filter_selected) {
        switch (selected_filter) {
            case 'search_questionnaire_status_select':
                window.location.href = url_search_questionnaire_status;
                break;
            case 'search_employees_select':
                window.location.href = url_search_employees;
                break;
            default:
                break;

        }
    }
})


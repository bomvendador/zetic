
process_table_clear('#table_questionnaire_status_search')

$('#start_questionnaire_status_search').on('click', function () {
    let company_id = $('#select_company').val()
    let status = $('#select_status').val()
    if (status === 'not_selected') {
        toastr.error('Выбериет статус опросника')
    } else {
        btn_spinner('#start_questionnaire_status_search')
        $.ajax({
            headers: {"X-CSRFToken": token},
            url: url_search_for_questionnaire_status,
            type: 'POST',
            data: JSON.stringify({
                'company_id': company_id,
                'status': status,
            }),
            processData: false,
            contentType: false,
            error: function (data) {
                toastr.error('Ошибка', data)
            },
            success: function (data) {
                btn_text('#start_questionnaire_status_search', 'Начать поиск')
                $('#table_questionnaire_status_search').DataTable().destroy()
                $('#table_questionnaire_status_search_tbody').html(data['rows'])
                process_table_clear('#table_questionnaire_status_search')
            }
        });


    }
})




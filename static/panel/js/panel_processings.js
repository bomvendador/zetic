expand_menu_item('#menu_processing')

$('#process_report_option').on('click', function () {
    btn_spinner($('#process_report_option'))
    $.ajax({
        headers: {"X-CSRFToken": token},
        url: url_run_processing,
        type: 'POST',
        data: JSON.stringify({
            'button_id': 'process_report_option',
            'name': 'Опции в отчетах',
        }),
        processData: false,
        contentType: false,
        error: function (data) {
            toastr.error('Ошибка', data)
        },
        success: function (data) {
            btn_text('#process_report_option', 'Опции в отчетах')
            toastr.success('Данные сохранены')
        }
    })
})
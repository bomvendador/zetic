process_table_clear('#table_report_1')

$('#report_description').text('Список опросников, заполнение которых было завершено')

$(document).ready(function () {
    $(".select-2-custom").select2();
});


$('#create_report_1').on('click', function () {
    let companies_ids = $('#companies').val()
    let gender_id = $('#gender').val()
    let date_from = $('#date_from').val()
    let date_to = $('#date_to').val()
    let age_from = $('#age_from').val()
    let age_to = $('#age_to').val()
    let roles_ids = $('#roles').val()
    let positions_ids = $('#positions').val()
    let industries_ids = $('#industries').val()
    let test_ok = true
    let only_relevant_reports = $('#only_relevant_reports').prop('checked')
    console.log('only_relevant_reports')
    console.log(only_relevant_reports)
    if (age_to < age_from) {
        toastr.error('Некорректный диапазон "Возраст респондента"')
        test_ok = false
    }
    let date_from_split = date_from.split('-')
    let date_to_split = date_to.split('-')
    let date_from_date = new Date(date_from_split[2], date_from_split[1], date_from_split[0])
    let date_to_date = new Date(date_to_split[2], date_to_split[1], date_to_split[0])
    if (date_to_date < date_from_date) {
        toastr.error('Некорректный диапазон "Дата окончания заполенения"')
        test_ok = false
    }
    if (test_ok) {
        btn_spinner('#create_report_1')
        $.ajax({
            headers: {"X-CSRFToken": token},
            url: url_create_statistics_report_1,
            type: 'POST',
            data: JSON.stringify({
                'companies_ids': companies_ids,
                'gender_id': gender_id,
                'date_from': date_from,
                'date_to': date_to,
                'age_from': age_from,
                'age_to': age_to,
                'roles_ids': roles_ids,
                'positions_ids': positions_ids,
                'industries_ids': industries_ids,
                'only_relevant_reports': only_relevant_reports,
            }),
            processData: false,
            contentType: false,
            error: function (data) {
                toastr.error('Ошибка', data)
            },
            success: function (data) {
                btn_text('#create_report_1', 'Сформировать отчет')
                let response = data['response']
                if (response['access_error']) {
                    toastr.error(response['access_error'])
                } else {
                    $('#table_report_1').DataTable().destroy()
                    if (response['rows']) {
                        $('#table_report_1_tbody').html(response['rows'])
                    } else {
                        $('#table_report_1_tbody').html('')
                    }


                    process_table_clear_with_excel_btn('#table_report_1', $('#statistics_reports_report_type_select_filter option:selected').text())
                    toastr.success('Отчет сформирован')
                }
            }
        });

    }
})

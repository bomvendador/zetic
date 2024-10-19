expand_menu_item('#menu_consultant_form_list')

let table = $('#table_consultant_forms').DataTable({
    buttons: ['excelHtml5', 'pdf'],
    language: {
        // searchPlaceholder: 'Поиск...',
        dom: 'Blfrtip',
        "url": "//cdn.datatables.net/plug-ins/9dcbecd42ad/i18n/Russian.json",
        scrollX: "100%",
        sSearch: 'Поиск',
    },
    'columnDefs': [
        {'targets': 'no-sort', 'orderable': false}
    ]
});
// table.buttons().container().appendTo('#table_questionnaire_status_search_wrapper .col-md-6:eq(0)');


$('#start_consultant_forms_search').on('click', function () {
    let company_id = $('#select_company').val()
    btn_spinner('#start_consultant_forms_search')
    $.ajax({
        headers: {"X-CSRFToken": token},
        url: url_get_consultant_forms,
        type: 'POST',
        data: JSON.stringify({
            'company_id': company_id,
        }),
        processData: false,
        contentType: false,
        error: function (data) {
            toastr.error('Ошибка', data)
        },
        success: function (data) {
            btn_text('#start_consultant_forms_search', 'Начать поиск')
            let rows = data['rows']
            // console.log(consultant_forms)
            $('#table_consultant_forms').DataTable().destroy()
            $('#table_consultant_forms_tbody').html(data['rows'])
            $('#table_consultant_forms').DataTable({
                buttons: ['excelHtml5', 'pdf'],
                language: {
                    // searchPlaceholder: 'Поиск...',
                    dom: 'Blfrtip',
                    "url": "//cdn.datatables.net/plug-ins/9dcbecd42ad/i18n/Russian.json",
                    scrollX: "100%",
                    sSearch: 'Поиск',
                },
                'columnDefs': [
                    {
                        'targets': 'no-sort',
                        'orderable': false
                    }
                ]
            });
            // process_table_clear('#table_consultant_forms')
        }
    });
})

$('body').on('click', '.delete-consultant-form', function () {
    let output_html = '<h2 class="mb-0" style="text-align: center">Удаление анкеты</h2>' +
        '<br>' +
        '<hr class="solid mt-0" style="background-color: black;">' +
        '<h4 style="text-align: center">Удалить анкету?</h4>' +
        '<hr class="solid mt-0" style="background-color: black;">'
    Swal.fire({
        html: output_html,
        icon: 'question',
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Да',
        cancelButtonText: 'Нет',
        showCancelButton: true
    }).then((result) => {
        if (result.value) {

            let form_node_tr = $(this).closest('tr')
            let form_id = form_node_tr.data('form-id')
            show_progressbar_loader()
            $.ajax({
                headers: {"X-CSRFToken": token},
                url: url_delete_consultant_form,
                type: 'POST',
                data: JSON.stringify({
                    'form_id': form_id,
                }),
                processData: false,
                contentType: false,
                error: function (data) {
                    toastr.error('Ошибка', data)
                },
                success: function (data) {
                    hide_progressbar_loader()
                    $('#table_consultant_forms').DataTable().destroy()
                    form_node_tr.remove()
                    process_table_clear('#table_consultant_forms')
                    toastr.success('Анкета удалена')
                }
            });

        }
    })


})

$('#select_all_consultant_forms_for_group_action').on('click', function () {
    if ($(this).prop('checked')) {
        $('.select-consultant-form-for-group-action').prop('checked', true)
        if ($('.select-consultant-form-for-group-action').length > 0) {
            $('#select_group_action_consultant_form').prop('disabled', false)
            $('#run_group_action_consultant_forms').prop('disabled', false)
        }

    } else {
        $('#select_group_action_consultant_form').prop('disabled', true)
        $('#run_group_action_consultant_forms').prop('disabled', true)

        $('.select-consultant-form-for-group-action').prop('checked', false)

    }
})

$('body').on('click', '.select-consultant-form-for-group-action', function () {
    if ($('.select-consultant-form-for-group-action:checked').length === 0) {
        $('#select_all_consultant_forms_for_group_action').prop('checked', false)
        $('#select_group_action_consultant_form').prop('disabled', true)
        $('#run_group_action_consultant_forms').prop('disabled', true)

    } else {
        $('#select_group_action_consultant_form').prop('disabled', false)
        $('#run_group_action_consultant_forms').prop('disabled', false)

    }
})

$('#run_group_action_consultant_forms').on('click', function () {
    let action = $('#select_group_action_consultant_form').val()
    switch (action) {
        case 'no_action':
            toastr.error('Выберите действие')

            break;
        case 'send_report_with_consultant_form':
            let forms_ids_to_send = []
            let forms_ids_not_to_send = []
            $('.select-consultant-form-for-group-action:checked').each(function () {
                let sent_emails = $(this).closest('tr').find('.sent_emails')
                console.log(sent_emails.html().trim())
                if (sent_emails.html().trim() === '') {
                    forms_ids_to_send.push($(this).closest('tr').data('form-id'))
                } else {
                    forms_ids_not_to_send.push($(this).closest('tr').data('form-id'))
                }
            })
            if (forms_ids_not_to_send.length > 0 && forms_ids_to_send.length === 0) {
                toastr.error('Выбранным респондентам уже был отправлен обновленный отчет')
            }
            console.log(forms_ids_not_to_send)
            if (forms_ids_to_send.length > 0) {
                show_progressbar_loader()
                $.ajax({
                    headers: {"X-CSRFToken": token},
                    url: url_send_report_to_participant_with_consultant_text,
                    type: 'POST',
                    data: JSON.stringify({
                        'forms_ids_to_send': forms_ids_to_send,
                    }),
                    processData: false,
                    contentType: false,
                    error: function (data) {
                        toastr.error('Ошибка', data)
                    },
                    success: function (data) {
                        hide_progressbar_loader()
                        let output_html = '<h2 class="mb-0" style="text-align: center">Запрос на сервер отправлен</h2>' +
                            '<br>' +
                            '<hr class="solid mt-0" style="background-color: black;">' +
                            '<h4 style="text-align: center">По завершению отправки на почту info@zetic.ru будет отправлен отчет с результатами выполнения</h4>' +
                            '<hr class="solid mt-0" style="background-color: black;">'

                        Swal.fire({
                            html: output_html,
                            icon: 'success',
                            confirmButtonColor: '#3085d6',
                            cancelButtonColor: '#d33',
                            confirmButtonText: 'ОК'
                        }).then((result) => {
                            if (result.value) {
                                window.location.reload()
                            }
                        })
                        //
                        // console.log(data)
                        // toastr.success('Доставлено')
                    }
                });

            }
            break;

        default:
            break;
    }
})
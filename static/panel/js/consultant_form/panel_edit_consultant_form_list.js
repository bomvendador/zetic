expand_menu_item('#menu_consultant_form_list')

let date = new Date();
date.setDate(date.getDate());

$.datepicker.regional['ru'] = {
    maxDate: date,
    closeText: 'Закрыть',
    prevText: 'Предыдущий',
    nextText: 'Следующий',
    currentText: 'Сегодня',
    monthNames: ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'],
    monthNamesShort: ['Янв', 'Фев', 'Мар', 'Апр', 'Май', 'Июн', 'Июл', 'Авг', 'Сен', 'Окт', 'Ноя', 'Дек'],
    dayNames: ['воскресенье', 'понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота'],
    dayNamesShort: ['вск', 'пнд', 'втр', 'срд', 'чтв', 'птн', 'сбт'],
    dayNamesMin: ['Вс', 'Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб'],
    weekHeader: 'Не',
    dateFormat: 'dd.mm.yy',
    firstDay: 1,
    isRTL: false,
    showMonthAfterYear: false,
    yearSuffix: ''
};
$.datepicker.setDefaults($.datepicker.regional['ru']);

$('.datepicker').datepicker();

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

$('#select_group_action_consultant_form').on('change', function () {
    if ($(this).val() === 'download_consultant_forms') {
        $('#dates_block').removeClass('d-none')
    } else {
        $('#dates_block').addClass('d-none')
    }
})


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

        case 'download_consultant_forms':
            let date_from = $('#date_from').datepicker("getDate")
            let date_to = $('#date_to').datepicker("getDate")
            let test_ok = true
            if (date_to !== null && date_from !== null) {
                if (date_from > date_to) {
                    toastr.error("Дата С должна быть больше даты ПО")
                    test_ok = false
                }

            }
            if (test_ok) {
                let forms_ids = []
                $('.select-consultant-form-for-group-action:checked').each(function () {
                    forms_ids.push($(this).closest('tr').data('form-id'))
                })

                $.ajax({
                    headers: {"X-CSRFToken": token},
                    url: url_download_consultant_forms,
                    type: 'POST',
                    data: JSON.stringify({
                        'date_from': $('#date_from').val(),
                        'date_to': $('#date_to').val(),
                        'forms_ids': forms_ids
                    }),
                    processData: false,
                    contentType: false,
                    error: function (data) {
                        toastr.error('Ошибка', data)
                    },
                    success: function (data) {
                        // console.log(data)
                        hide_progressbar_loader()
                        let response = data['response']
                        let header = ['ФИО', 'Email', 'Компания', 'Год рождения', 'Роль', 'Позиция', 'Индустрия', 'Пол', 'Дата создания анкеты', 'Специальные комментарии', 'Риски', 'Карьерный трек', 'Тип светофора', 'Светофор', 'Комментарии']
                        let rows = []
                        rows.push(header)
                        response.forEach(function (form) {
                            // console.log(form)
                            let participant = form['participant']
                            let form_data = form['form_data']
                            let participant_for_row = [participant['fio'], participant['email'], participant['company_name'], participant['birth_year'], participant['role_name'], participant['position'], participant['industry'], participant['gender']]
                            let form_data_for_row = [form_data['created_at'], form_data['special_comments'], form_data['risks'], form_data['career_track']]


                            let consultant_texts = form['consultant_texts']
                            consultant_texts.forEach(function (text) {
                                let row = []
                                row.push(...participant_for_row)
                                row.push(...form_data_for_row)

                                let comments_data = text['comments_data']
                                let comments_string = ''
                                comments_data.forEach(function (comment) {
                                    comments_string += '[' + comment + ']'
                                })
                                row.push(text['type'], text['name'], comments_string)
                                rows.push(row)
                            })


                        })

                        let workbook = XLSX.utils.book_new(), worksheet = XLSX.utils.aoa_to_sheet(rows);
                        workbook.SheetNames.push("Анкеты");
                        workbook.Sheets["Анкеты"] = worksheet;
                        let currentdate = new Date();
                        let datetime_string = currentdate.getDate() + '_'
                            + (currentdate.getMonth() + 1).toString() + '_'
                            + currentdate.getFullYear() + " @ "
                            + currentdate.getHours() + ":"
                            + currentdate.getMinutes() + ":"
                            + currentdate.getSeconds();
                        XLSX.writeFile(workbook, '[Анкеты] ' + datetime_string + ".xlsx");

                    }
                });


            }

            break;
        default:
            break;
    }
})
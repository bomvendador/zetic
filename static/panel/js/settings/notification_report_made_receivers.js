expand_menu_item('#menu_settings')

$('#add_common_report_made_notification_receiver').on('click', function () {
    let available_receivers_qnt = $('#common_report_made_notification_receiver_select option').length
    if (available_receivers_qnt > 1) {
        $('#input_modal_common_report_made_notification_receiver').modal('show')
        // $("#company_report_made_notification_receiver_select").select2("destroy").select2();
    } else {
        toastr.warning('Все сотрудники уже были добавлены')
    }
})

$('#save_common_report_made_notification_receiver_btn').on('click', function () {
    let value = $('#common_report_made_notification_receiver_select option:selected').val()
    console.log(value)
    if (value === '0') {
        toastr.error('Выберите получателя')
    } else {
        btn_spinner($('#save_common_report_made_notification_receiver_btn'))
        $.ajax({
            headers: {"X-CSRFToken": token},
            url: url_add_common_report_made_notification_receiver,
            type: 'POST',
            data: JSON.stringify({
                'user_id': value,
            }),
            processData: false,
            contentType: false,
            error: function (data) {
                toastr.error('Ошибка', data)
            },
            success: function (data) {
                btn_text($('#save_common_report_made_notification_receiver_btn'), 'Сохранить')
                $('#input_modal_common_report_made_notification_receiver').modal('hide')
                let output_html = '<hr class="solid mt-0" style="background-color: black;">' +
                    '<h3 style="text-align: center">Получатель добавлен</h3>' +
                    '<hr class="solid mt-0" style="background-color: black;">'
                Swal.fire({
                    html: output_html,
                    icon: 'success',
                    confirmButtonColor: '#3085d6',
                    cancelButtonColor: '#d33',
                    confirmButtonText: 'Ок',
                }).then((result) => {
                    if (result.value) {
                        window.location.reload()
                    }
                })


            }
        });

    }
})

$('.delete-notification-receiver').on('click', function () {
    let output_html = '<h2 class="mb-0" style="text-align: center">Удаление получателя уведомления об отчете</h2>' +
        '<br>' +
        '<hr class="solid mt-0" style="background-color: black;">' +
        '<h4 style="text-align: center">Удалить получателя?</h4>' +
        '<hr class="solid mt-0" style="background-color: black;">'
    Swal.fire({
        html: output_html,
        icon: 'question',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Да',
        cancelButtonText: 'Нет'
    }).then((result) => {
        if (result.value) {
            let receiver_id = $(this).closest('tr').data('receiver-id')
            show_progressbar_loader()
            $.ajax({
                headers: {"X-CSRFToken": token},
                url: url_delete_common_report_made_notification_receiver,
                type: 'POST',
                data: JSON.stringify({
                    'receiver_id': receiver_id,
                }),
                processData: false,
                contentType: false,
                error: function (data) {
                    toastr.error('Ошибка', data)
                },
                success: function (data) {
                    hide_progressbar_loader()
                    $('#input_modal_report_made_notification_receiver').modal('hide')
                    let output_html = '<hr class="solid mt-0" style="background-color: black;">' +
                        '<h3 style="text-align: center">Получатель удален</h3>' +
                        '<hr class="solid mt-0" style="background-color: black;">'
                    Swal.fire({
                        html: output_html,
                        icon: 'success',
                        confirmButtonColor: '#3085d6',
                        cancelButtonColor: '#d33',
                        confirmButtonText: 'Ок',
                    }).then((result) => {
                        if (result.value) {
                            window.location.reload()
                        }
                    })


                }
            });
        }
    })


})

$('#appoint_company_admin').on('click', function () {
    let test_ok = true
    let pwd = $('#new_password').val()
    let pwd_confirm = $('#new_password_confirm').val()
    let employee_id = $('#company_admin_select option:selected').attr('id').split('_')[2]
    if (pwd === '' || pwd_confirm === '') {
        toastr.error('Поля паролей должны быть заполнены')
        test_ok = false
    } else {
        if (pwd !== pwd_confirm) {
            toastr.error('Пароли не совпадают')
            test_ok = false
        }
    }
    if (test_ok) {
        btn_spinner($('#appoint_company_admin'))
        $.ajax({
            headers: {"X-CSRFToken": token},
            url: url_appoint_company_admin,
            type: 'POST',
            data: JSON.stringify({
                'employee_id': employee_id,
                'password': pwd
            }),
            processData: false,
            contentType: false,
            error: function (data) {
                toastr.error('Ошибка', data)
            },
            success: function (data) {
                let data_json = data['data']
                let html = ''
                html += '<tr id="employee_id_' + data["id"] + '">'
                html += '<td>' + data['name'] + '</td>'
                html += '<td>' + data['email'] + '</td>'
                html += '<td><span class="dot-label bg-success" title="Админ активен"></span></td>'
                html += '<td><div style="text-align: center;">' +
                    '<i class="fe fe-more-vertical cursor-pointer" data-bs-toggle="dropdown" aria-expanded="false" style="font-size: 20px"></i>' +
                    '<ul class="dropdown-menu">' +
                    '<li><a class="dropdown-item deactivate-company-admin cursor-pointer">Деактивировать</a></li>' +
                    '<li><a class="dropdown-item delete-company-admin cursor-pointer">Удалить</a></li>' +
                    '</ul>' +
                    '</div>' +
                    '</td>'
                html += '</tr>'
                $('#tbody_company_admins').find('.no-data-text').each(function (index, el) {
                    $(el).closest('tr').remove()
                })
                $('#tbody_company_admins').append(html)
                $('#input_modal_add_admin').modal('hide')
                btn_text($('#appoint_company_admin'), 'Сохранить')

                toastr.success('Админ назначен')

            }
        });
    }
})

$('#tbody_company_admins').on('click', '.deactivate-company-admin', function () {
    let operation_name = $(this).text().trim()
    let operation_type = ''
    let question_text = ''
    let resul_text = ''
    let btn_text = ''
    let icon_add_class = ''
    let icon_remove_class = ''
    if (operation_name === 'Деактивировать') {
        console.log('Деактивировать')
        question_text = 'Деактивировать админа?'
        resul_text = 'Админ деактивирован'
        btn_text = 'Активировать'
        icon_add_class = 'bg-danger'
        icon_remove_class = 'bg-success'
        operation_type = 'deactivate'
    } else {
        console.log('Активировать')
        question_text = 'Активировать админа?'
        operation_type = 'activate'
        resul_text = 'Админ активирован'
        btn_text = 'Деактивировать'
        icon_add_class = 'bg-success'
        icon_remove_class = 'bg-danger'
    }

    let tr_id = $(this).closest('tr').attr('id')
    let employee_id = $(this).closest('tr').attr('id').split('_')[2]
    let employee_name = $(this).closest('tr td:first-child').text()
    let output_html = '<hr class="solid mt-0" style="background-color: black;">' +
        '<div>' + question_text + '</div>' +
        '<br>' +
        '<hr class="solid mt-0" style="background-color: black;">'
    Swal.fire({
        html: output_html,
        icon: 'question',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Да',
        cancelButtonText: 'Нет'
    }).then((result) => {
        if (result.value) {
            show_progressbar_loader()
            $.ajax({
                headers: {"X-CSRFToken": token},
                url: url_deactivate_company_admin,
                type: 'POST',
                data: JSON.stringify({
                    'employee_id': employee_id,
                    'operation_type': operation_type
                }),
                processData: false,
                contentType: false,
                error: function (data) {
                    toastr.error('Ошибка', data)
                },
                success: function (data) {
                    // let el = $('#' + tr_id).find('.dot-label')
                    let el = $('#' + tr_id)
                    el.find('.dot-label').removeClass(icon_remove_class).addClass(icon_add_class)
                    console.log('btn_text = ' + btn_text)
                    el.find('.deactivate-company-admin').text(btn_text)

                    toastr.success(resul_text)
                    hide_progressbar_loader()
                }
            });


        }
    })

    console.log(employee_id)

})

$('#tbody_company_admins').on('click', '.delete-company-admin', function () {
    let tr = $(this).closest('tr')
    let employee_id = $(this).closest('tr').attr('id').split('_')[2]
    let output_html = '<hr class="solid mt-0" style="background-color: black;">' +
        '<div>Удалить админа?</div>' +
        '<br>' +
        '<hr class="solid mt-0" style="background-color: black;">'
    Swal.fire({
        html: output_html,
        icon: 'question',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Да',
        cancelButtonText: 'Нет'
    }).then((result) => {
        if (result.value) {
            show_progressbar_loader()
            $.ajax({
                headers: {"X-CSRFToken": token},
                url: url_delete_company_admin,
                type: 'POST',
                data: JSON.stringify({
                    'employee_id': employee_id,
                }),
                processData: false,
                contentType: false,
                error: function (data) {
                    toastr.error('Ошибка', data)
                },
                success: function (data) {
                    tr.remove()
                    console.log($('#tbody_company_admins tr').length)
                    if ($('#tbody_company_admins tr').length === 0) {
                        $('#tbody_company_admins').html('<tr><td class="no-data-text" colspan="4">Админы не назначены</td></tr>')
                    }

                    toastr.success("Админ удален")
                    hide_progressbar_loader()
                }
            });


        }
    })


})


$('#company_active').on('click', function () {
    if ($(this).attr('checked') === 'checked') {
        $(this).attr('checked', false)
        active = 0
    } else {
        $(this).attr('checked', 'checked')
        active = 1
    }
})

$('#update_company').on('click', function () {
    let company_name = $('#input_company_name').val()
    let demo_limit = ''
    let test_ok = true

    if (company_name === '') {
        toastr.error('Название компании не заполнено')
        test_ok = false
    }
    if ($('#company_demo_status_limit').length) {
        if ($('#company_demo_status_limit').val() === '') {
            toastr.error('Ограничение по кол-ву опросников не заполнено')
            test_ok = false
        } else {
            demo_limit = $('#company_demo_status_limit').val()
        }
    }

    if (test_ok) {
        btn_spinner($('#save_company'))
        $.ajax({
            headers: {"X-CSRFToken": token},
            url: url_update_company,
            type: 'POST',
            data: JSON.stringify({
                'company_name': company_name,
                'company_id': company_id,
                'active': active,
                'demo_status': $('#company_demo_status').prop('checked'),
                'demo_limit': demo_limit
            }),
            processData: false,
            contentType: false,
            error: function (data) {
                toastr.error('Ошибка', data)
            },
            success: function (data) {
                toastr.success('Данные сохранены')
                btn_text($('#save_company'), 'Сохранить')
            }
        });
    }


})

$('#delete_company').on('click', function () {
    let output_html = '<hr class="solid mt-0" style="background-color: black;">' +
        '<div>Удалить компанию?</div>' +
        '<br>' +
        '<hr class="solid mt-0" style="background-color: black;">'
    Swal.fire({
        html: output_html,
        icon: 'question',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Да',
        cancelButtonText: 'Нет'
    }).then((result) => {
        if (result.isConfirmed) {
            show_progressbar_loader()
            $.ajax({
                headers: {"X-CSRFToken": token},
                url: url_delete_company,
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
                    window.location.href = url_companies_list
                }
            });

        }
    })

})
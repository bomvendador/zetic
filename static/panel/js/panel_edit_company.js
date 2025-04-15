expand_menu_item('#menu_companies_list')

$('.self-questionnaire-link-status').on('click', function () {
    let node = $(this)
    let link_id = node.closest('tr').data('link-id')
    let operation = node.data('operation')
    let question_text = ''
    if (operation === 'block') {
        question_text = 'Заблокировать ссылку?'
    } else {
        question_text = 'Разблокировать ссылку?'
    }
    let output_html = '<h2 class="mb-0" style="text-align: center">Изменение доступности ссылки</h2>' +
        '<br>' +
        '<hr class="solid mt-0" style="background-color: black;">' +
        '<h4 style="text-align: center">' + question_text + '</h4>' +
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
        let change_participants_individual_report_options = false
        if (result.value) {
            change_participants_individual_report_options = true
            show_progressbar_loader()
            $.ajax({
                headers: {"X-CSRFToken": token},
                url: url_change_self_questionnaire_link_active_field,
                type: 'POST',
                data: JSON.stringify({
                    'link_id': link_id,
                    'operation': operation,
                }),
                processData: false,
                contentType: false,
                error: function (data) {
                    toastr.error('Ошибка', data)
                },
                success: function (data) {
                    hide_progressbar_loader()
                    let output_html = '<h2 class="mb-0" style="text-align: center">Данные сохранены</h2>' +
                        '<br>' +
                        '<hr class="solid mt-0" style="background-color: black;">' +
                        '<h4 style="text-align: center">Данные ссылки обновлены</h4>' +
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


                }
            });

        }


    })

})

$('.update_company_report_options_allowed_btn').on('click', function (event) {
    let node_btn = $(this)

    let output_html = '<h2 class="mb-0" style="text-align: center">Изменение индивидуальных настроек</h2>' +
        '<br>' +
        '<hr class="solid mt-0" style="background-color: black;">' +
        '<h4 style="text-align: center">Изменить настройки всех существующих участников опросов?</h4>' +
        '<hr class="solid mt-0" style="background-color: black;">' +
        '<h5 style="text-align: center; color: red">Внимание! Настройки ВСЕХ респондентов будут изменены</h5>' +
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
        let change_participants_individual_report_options = false
        if (result.value) {
            change_participants_individual_report_options = true
        }

        btn_spinner(node_btn)
        let options_vals = []
        node_btn.closest('.card').find('.option-switch').each(function () {
            // console.log(`${$(this).data("option-id")} ${$(this).prop('checked')}`)
            options_vals.push({
                'type': $(this).data("type"),
                'id': $(this).data("option-id"),
                'value': $(this).prop('checked'),
            })
        })
        // console.log(options_vals)
        btn_spinner('#update_company_individual_report_options_allowed')

        $.ajax({
            headers: {"X-CSRFToken": token},
            url: url_update_company_report_options_allowed,
            type: 'PUT',
            data: JSON.stringify({
                'options_vals': options_vals,
                'company_id': company_id,
                'change_participants_individual_report_options': change_participants_individual_report_options,
            }),
            processData: false,
            contentType: false,
            error: function (data) {
                toastr.error('Ошибка', data)
            },
            success: function (data) {
                btn_text(node_btn, 'Сохранить')
                toastr.success('Данные сохранены')

            }
        });


    })
})


$('.copy-company-questionnaire-link').on('click', function (e) {
    e.preventDefault();
    let text = window.location.origin + $(this).closest('div').find('a').attr('href');
    try {
        navigator.clipboard.writeText(text).then(r => {
            toastr.success('Ссылка скопирована')
        })

    } catch (e) {
        toastr.warning('Копирование возможно при наличии SSL')
        // console.log(e)
    }
})


$('.add-consultant-study').on('click', function () {
    show_progressbar_loader()
    let consultant_company_id = $(this).closest('tr').data('consultant-company-id')

    $.ajax({
        headers: {"X-CSRFToken": token},
        url: url_get_available_consultant_company_studies,
        type: 'POST',
        data: JSON.stringify({
            'consultant_company_id': consultant_company_id,
        }),
        processData: false,
        contentType: false,
        error: function (data) {
            toastr.error('Ошибка', data)
        },
        success: function (data) {
            hide_progressbar_loader()
            let studies = data['studies']
            console.log(data)
            if (studies.length > 0) {
                studies.forEach(function (study) {
                    $('#consultant_study_select').append('<option value="' + study['id'] + '">' + study['id'] + '. ' + study['name'] + '</option>')
                })
                $('#consultant_study_select').attr('data-consultant-company-id', data['consultant_company_id'])
                $('#input_modal_consultant_study').modal('show')

            } else {
                toastr.warning('Доступные исследования отсутствуют')
            }

        }
    });

})


$('#save_consultant_study_for_company_btn').on('click', function () {
    let study_id = $('#consultant_study_select').val()
    let consultant_company_id = $('#consultant_study_select').data('consultant-company-id')
    if (study_id === '0') {
        toastr.error('Выберите исследование')
    } else {
        btn_spinner('#save_consultant_study_for_company_btn')
        $.ajax({
            headers: {"X-CSRFToken": token},
            url: url_add_consultant_study_for_company,
            type: 'POST',
            data: JSON.stringify({
                'study_id': study_id,
                'consultant_company_id': consultant_company_id,
            }),
            processData: false,
            contentType: false,
            error: function (data) {
                toastr.error('Ошибка', data)
            },
            success: function (data) {
                btn_text('#save_consultant_for_company_btn', 'Сохранить')

                let output_html = '<h2 class="mb-0" style="text-align: center">Данные сохранены</h2>' +
                    '<br>' +
                    '<hr class="solid mt-0" style="background-color: black;">' +
                    '<h4 style="text-align: center">Исследование успешно добавлено</h4>' +
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


            }
        });

    }
})

$('.delete-consultant-study').on('click', function () {
    let output_html = '<h2 class="mb-0" style="text-align: center">Удаление исследование консультанта</h2>' +
        '<br>' +
        '<hr class="solid mt-0" style="background-color: black;">' +
        '<h4 style="text-align: center">Удалить исследование?</h4>' +
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
            let consultant_study_id = $(this).data('consultant-study-id')
            $.ajax({
                headers: {"X-CSRFToken": token},
                url: url_delete_consultant_study_from_company,
                type: 'POST',
                data: JSON.stringify({
                    'consultant_study_id': consultant_study_id,
                }),
                processData: false,
                contentType: false,
                error: function (data) {
                    toastr.error('Ошибка', data)
                },
                success: function (data) {
                    hide_progressbar_loader()

                    let output_html = '<h2 class="mb-0" style="text-align: center">Данные сохранены</h2>' +
                        '<br>' +
                        '<hr class="solid mt-0" style="background-color: black;">' +
                        '<h4 style="text-align: center">Исследование успешно удалено</h4>' +
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


                }
            });

        }
    })
})

$('#add_consultant').on('click', function () {
    show_progressbar_loader()
    $.ajax({
        headers: {"X-CSRFToken": token},
        url: url_get_available_consultants,
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
            hide_progressbar_loader()
            let consultants = data['consultants']
            console.log(data)
            if (consultants.length > 0) {
                consultants.forEach(function (consultant) {
                    $('#consultant_select').append('<option value="' + consultant['user_id'] + '">' + consultant['name'] + ' - ' + consultant['email'] + '</option>')
                })
                $('#input_modal_consultants').modal('show')

            } else {
                toastr.warning('Доступные консультанты отсутствуют')
            }

        }
    });

})

$('.delete-consultant').on('click', function () {
    let output_html = '<h2 class="mb-0" style="text-align: center">Удаление консультанта</h2>' +
        '<br>' +
        '<hr class="solid mt-0" style="background-color: black;">' +
        '<h4 style="text-align: center">Удалить консультанта?</h4>' +
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
            let consultant_company_id = $(this).closest('tr').data('consultant-company-id')
            $.ajax({
                headers: {"X-CSRFToken": token},
                url: url_delete_consultant_fromm_company,
                type: 'POST',
                data: JSON.stringify({
                    'consultant_company_id': consultant_company_id,
                }),
                processData: false,
                contentType: false,
                error: function (data) {
                    toastr.error('Ошибка', data)
                },
                success: function (data) {
                    hide_progressbar_loader()

                    let output_html = '<h2 class="mb-0" style="text-align: center">Данные сохранены</h2>' +
                        '<br>' +
                        '<hr class="solid mt-0" style="background-color: black;">' +
                        '<h4 style="text-align: center">Консультант успешно удалён</h4>' +
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


                }
            });

        }
    })
})

$('#save_consultant_for_company_btn').on('click', function () {
    let user_id = $('#consultant_select').val()
    if (user_id === '0') {
        toastr.error('Выберите консультанта')
    } else {
        btn_spinner('#save_consultant_for_company_btn')
        $.ajax({
            headers: {"X-CSRFToken": token},
            url: url_add_consultant_for_company,
            type: 'POST',
            data: JSON.stringify({
                'company_id': company_id,
                'user_id': user_id,
            }),
            processData: false,
            contentType: false,
            error: function (data) {
                toastr.error('Ошибка', data)
            },
            success: function (data) {
                btn_text('#save_consultant_for_company_btn', 'Сохранить')

                let output_html = '<h2 class="mb-0" style="text-align: center">Данные сохранены</h2>' +
                    '<br>' +
                    '<hr class="solid mt-0" style="background-color: black;">' +
                    '<h4 style="text-align: center">Консультант успешно добавлен</h4>' +
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


            }
        });

    }
})

$('#new_password_hide').on('click', function () {
    let attr = $('#new_password').attr('type')
    if (typeof attr !== 'undefined') {
        $('#new_password').removeAttr('type')
        $(this).removeClass('zmdi-eye').addClass('zmdi-eye-off')

    } else {
        $('#new_password').attr('type', 'password')
        $(this).removeClass('zmdi-eye-off').addClass('zmdi-eye')
    }
})

$('#new_password_confirm_hide').on('click', function () {
    let attr = $('#new_password_confirm').attr('type')
    if (typeof attr !== 'undefined') {
        $('#new_password_confirm').removeAttr('type')
        $(this).removeClass('zmdi-eye').addClass('zmdi-eye-off')
    } else {
        $('#new_password_confirm').attr('type', 'password')
        $(this).removeClass('zmdi-eye-off').addClass('zmdi-eye')
    }
})

$('#select_link_template_btn').on('click', function () {
    $('#select_template option').attr('selected', false)
    $('#select_template option').eq(0).attr('selected', true)
    $('#input_modal_select_link_template').modal('show')
})

$('#generate_link').on('click', function () {
    let option_val = $('#select_template option:selected').val()
    if (option_val == 0) {
        toastr.error('Выберите шаблон')
    } else {
        btn_spinner('#generate_link')
        $.ajax({
            headers: {"X-CSRFToken": token},
            url: url_generate_new_self_questionnaire_link,
            type: 'POST',
            data: JSON.stringify({
                'company_id': company_id,
                'template_id': option_val
            }),
            processData: false,
            contentType: false,
            error: function (data) {
                toastr.error('Ошибка', data)
            },
            success: function (data) {
                let code = data['code']
                console.log(code)
                console.log(window.location.hostname)
                console.log(window.location.protocol)
                // let link = `${window.location.protocol}//${window.location.hostname}/company_questionnaire/${code}`
                let link = `${window.location.origin}/panel/company_questionnaire/${code}`
                console.log(link)
                let output_html = '<h2 class="mb-0" style="text-align: center">Данные сохранены</h2>' +
                    '<br>' +
                    '<hr class="solid mt-0" style="background-color: black;">' +
                    '<h4 style="text-align: center">Ссылка успешно добавлена</h4>' +
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


                // $('#company_admin_select').html(html)
                // console.log(data_json)
                // $('#input_modal_add_admin').modal('show')
                btn_text($('#generate_link'), 'Создать ссылку')

            }
        });
    }
})

$('#tbody_self_questionnaire_link input').each(function () {
    let val = $(this).val()
    let full_link = `${window.location.origin}${val}`
    $(this).val(full_link)
})

$('#add_admin').on('click', function () {
    btn_spinner($('#add_admin'))
    $.ajax({
        headers: {"X-CSRFToken": token},
        url: url_get_company_no_admins,
        type: 'POST',
        data: JSON.stringify({
            'company_id': company_id
        }),
        processData: false,
        contentType: false,
        error: function (data) {
            toastr.error('Ошибка', data)
        },
        success: function (data) {
            let data_json = data['data']
            let html = ''
            for (let i = 0; i < data_json.length; i++) {
                console.log(data_json[i]["name"])
                html += '<option id="employee_id_' + data_json[i]["id"] + '">' + data_json[i]["name"] + '</option>>'
                // html += '<option>' + data_json[i]["email"] + '</option>'
                // if(data_json[i]["active"]){
                //     html += '<option><span class="dot-label bg-success" title="Админ активен"></span></option>'
                // }else {
                //     html += '<option><span class="dot-label bg-danger" title="Админ активен"></span></option>'
                //
                // }
            }
            $('#company_admin_select').html(html)
            $('#input_modal_add_admin').modal('show')
            btn_text($('#add_admin'), 'Назначить')

        }
    });
})

$('#add_report_made_notification_receiver').on('click', function () {
    let available_receivers_qnt = $('#company_report_made_notification_receiver_select option').length
    if (available_receivers_qnt > 1) {
        $('#input_modal_report_made_notification_receiver').modal('show')
        // $("#company_report_made_notification_receiver_select").select2("destroy").select2();
    } else {
        toastr.warning('Все сотрудники уже были добавлены')
    }
})

$('#save_report_made_notification_receiver_btn').on('click', function () {
    let value = $('#company_report_made_notification_receiver_select option:selected').val()
    console.log(value)
    if (value === '0') {
        toastr.error('Выберите получателя')
    } else {
        btn_spinner($('#save_report_made_notification_receiver_btn'))
        $.ajax({
            headers: {"X-CSRFToken": token},
            url: url_add_report_made_notification_receiver,
            type: 'POST',
            data: JSON.stringify({
                'employee_id': value,
            }),
            processData: false,
            contentType: false,
            error: function (data) {
                toastr.error('Ошибка', data)
            },
            success: function (data) {
                btn_text($('#save_report_made_notification_receiver_btn'), 'Сохранить')
                $('#input_modal_report_made_notification_receiver').modal('hide')
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
                url: url_delete_report_made_notification_receiver,
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
        '<div style="text-align: center">' + question_text + '</div>' +
        '<hr class="solid" style="background-color: black;">'
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
        '<h3 style="text-align: center">Удаление админа</h3>' +
        '<hr class="solid mt-0" style="background-color: black;">' +
        '<div style="text-align: center">Удалить админа?</div>'
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
$('#menu_users_list').closest('.slide').addClass('is-expanded')
$('#menu_users_list').addClass('active')

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

$('#save_password').on('click', function () {
    if ($('#new_password').val() !== $('#new_password_confirm').val()) {
        toastr.error('Пароли не совпадают')
    } else {
        btn_spinner($('#save_password'))
        $.ajax({
            headers: {"X-CSRFToken": token},
            url: url_save_user_pwd,
            type: 'POST',

            data: JSON.stringify({
                'user_id': user_id,
                'password': $('#new_password').val()
            }),
            processData: false,
            contentType: false,
            error: function (data) {
                toastr.error('Ошибка', data)
            },
            success: function (data) {
                btn_text($('#save_password'), 'Сохранить')
                toastr.success('Пароль обновлен')
            }
        });

    }
})
$('#save_info').on('click', function () {
    if ($('#new_password').val() !== $('#new_password_confirm').val()) {
        toastr.error('Пароли не совпадают')
    } else {
        if ($('#input_fio').val() === '' || $('#input_email').val() === '' || $('#input_tel').val() === '' || $('#user_role').find(':selected').text() === '') {
            toastr.error('Все поля должны быть заполнены')
        } else {
            btn_spinner($('#save_info'))
            $.ajax({
                headers: {"X-CSRFToken": token},
                url: url_save_user_profile,
                type: 'POST',

                data: JSON.stringify({
                    'user_id': user_id,
                    'user_fio': $('#input_fio').val(),
                    'user_email': $('#input_email').val(),
                    'user_tel': $('#input_tel').val(),
                    'user_role': $('#user_role').find(':selected').text()
                }),
                processData: false,
                contentType: false,
                error: function (data) {
                    toastr.error('Ошибка', data)
                },
                success: function (data) {
                    btn_text($('#save_info'), 'Сохранить')
                    toastr.success('Данные обновлены')
                    $('#contacts_email').text($('#input_email').val())
                    $('#contacts_tel').text($('#input_tel').val())
                    $('#password_card_fio').text($('#input_fio').val())
                    $('#password_card_role').text($('#user_role').find(':selected').text())
                }
            });

        }

    }
})

$('#delete_user').on('click', function () {
    if (user_id === cur_user_id) {
        Swal.fire({
            title: 'Пользователь не может быть удален',
            text: "Вы пытаетесь удалить свой собственный аккаунт, что невозможно из соображений безопасности",
            icon: 'error',
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'ОК'
        })

    } else {
        Swal.fire({
            title: 'Удаление пользователя',
            text: "Удалить пользователя?",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Да',
            cancelButtonText: 'Нет'
        }).then((result) => {
            if (result.value) {

                $.ajax({
                    headers: {"X-CSRFToken": token},
                    url: url_delete_user,
                    type: 'POST',

                    data: JSON.stringify({
                        'user_id': user_id,
                    }),
                    processData: false,
                    contentType: false,
                    error: function (data) {
                        toastr.error('Ошибка', data)
                    },
                    success: function (data) {
                        if (data === 'error') {
                            Swal.fire({
                                title: 'Ошибка при удалении',
                                text: "Пользователь не может быть удален",
                                icon: 'error',
                                confirmButtonColor: '#3085d6',
                                cancelButtonColor: '#d33',
                                confirmButtonText: 'ОК'
                            })
                        } else {
                            Swal.fire({
                                title: 'Пользователь удален',
                                text: "Все данные пользователя удалены",
                                icon: 'success',
                                confirmButtonColor: '#3085d6',
                                cancelButtonColor: '#d33',
                                confirmButtonText: 'ОК'
                            }).then((result) => {
                                if (result.value) {
                                    window.location.href = url_users_list
                                }
                            })

                        }

                    }
                });
            }
        })
    }
})

$('#add_user_company').on('click', function () {
    $('#select_company').select2({
        dropdownParent: $("#input_modal_add_user_company"),
        width: '100%'
    })
    $('#input_modal_add_user_company').modal('show')
})

$('#modal_add_user_company_btn').on('click', function () {
    let company_id = $('#select_company').val()
    $.ajax({
        headers: {"X-CSRFToken": token},
        url: url_add_user_company,
        type: 'POST',

        data: JSON.stringify({
            'user_id': user_id,
            'company_id': company_id
        }),
        processData: false,
        contentType: false,
        error: function (data) {
            toastr.error('Ошибка', data)
        },
        success: function (data) {
            let output_html = '<h2 class="mb-0" style="text-align: center">Данные сохранены</h2>' +
                '<br>' +
                '<hr class="solid mt-0" style="background-color: black;">' +
                '<h4 style="text-align: center">Компания добавлена</h4>' +
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

})

$('#select_company').on('change', function () {
    console.log($(this).val())
    if ($(this).val() !== '') {
        $('#modal_add_user_company_btn').prop('disabled', false)
    } else {
        $('#modal_add_user_company_btn').prop('disabled', true)

    }
})

$('#tbody_user_companies').on('click', '.delete-user-company', function () {
    let output_html = '<h2 class="mb-0" style="text-align: center">Удаление компании</h2>' +
        '<br>' +
        '<hr class="solid mt-0" style="background-color: black;">' +
        '<h4 style="text-align: center">Удалить компанию?</h4>' +
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
            show_progressbar_loader()
            let company_id = $(this).closest('tr').data('company-id')
            $.ajax({
                headers: {"X-CSRFToken": token},
                url: url_delete_user_company,
                type: 'POST',
                data: JSON.stringify({
                    'company_id': company_id,
                    'user_id': user_id
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
                        '<h4 style="text-align: center">Компания удалена</h4>' +
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
            })


        }
    })


})


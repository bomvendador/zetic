expand_menu_item('#menu_company_add')

let active = 1


$('#company_active').on('click', function () {
    console.log($(this).attr('checked'))
    if ($(this).attr('checked') === 'checked') {
        $(this).attr('checked', false)
        active = 0
    } else {
        $(this).attr('checked', 'checked')
        active = 1
    }
})

$('#save_company').on('click', function () {
    let test_ok = true
    let demo_limit = ''
    if ($('#input_company_name').val() === '') {
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
            url: url_save_new_company,
            type: 'POST',
            data: JSON.stringify({
                'name': $('#input_company_name').val(),
                'demo_limit': demo_limit,
                'active': active,
                'demo_status': $('#company_demo_status').prop('checked')
            }),
            processData: false,
            contentType: false,
            error: function (data) {
                toastr.error('Ошибка', data)
            },
            success: function (data) {
                console.log(data)
                btn_text($('#save_company'), 'Сохранить')
                if (data['error']) {
                    toastr.error(data['error'])
                } else {
                    let output_html = '<h2 class="mb-0" style="text-align: center">Данные сохранены</h2>' +
                        '<br>' +
                        '<hr class="solid mt-0" style="background-color: black;">' +
                        '<h4 style="text-align: center">Kомпания успешно создана</h4>' +
                        '<hr class="solid mt-0" style="background-color: black;">'

                    Swal.fire({
                        html: output_html,
                        icon: 'success',
                        confirmButtonColor: '#3085d6',
                        cancelButtonColor: '#d33',
                        confirmButtonText: 'ОК'
                    }).then((result) => {
                        if (result.value) {
                            window.location.href = url_companies_list
                        }
                    })

                }

            }
        });
    }
})

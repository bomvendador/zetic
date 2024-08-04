expand_menu_item('#menu_employee_add')


$(document).ready(function () {
    $(".yearpicker").yearpicker({
        // year: 2010,
        startYear: 1940,
        endYear: 2010,
    });
});

$('#employee_birth_year').keypress(function (e) {
    console.log(e.which)
    if (e.keyCode !== 13 || e.which !== 13) {
        e.preventDefault()
        return false
    }
})

let company_id

function route_menu_handler(route_index, btn_type) {
    let new_menu_number = 0
    if (btn_type === 'next') {
        new_menu_number = route_index + 1
    } else {
        new_menu_number = route_index - 1
    }
    console.log('new_menu_number - ' + new_menu_number)
    if (new_menu_number <= 4) {
        $('.route-item').each(function (i, obj) {
            if (parseInt($(this).find('.number').html()) !== new_menu_number) {
                $(this).addClass('disabled')
                $(this).removeClass('current')

            } else {
                $(this).removeClass('disabled')
                $(this).addClass('current')
            }
        })
        // if(new_menu_number === 3){
        //
        // }else {
        //     $('#next').removeClass('disabled')
        //
        // }

    } else {
        toastr.info('Конец')

    }
}


function route_handler(route_index) {
    console.log('project - ' + $('.company-chosen').text().trim())
    console.log('route_index - ' + route_index)
    btn_spinner($('#next'))
    switch (route_index) {
        case 1:
            company_id = $('.company-chosen').attr('id').split('_')[2].trim()

            $('#wizard1-h-1').css('display', 'block')
            $('#wizard1-p-1').css('display', 'block')
            $('#wizard1-h-0').css('display', 'none')
            $('#wizard1-p-0').css('display', 'none')

            btn_text($('#next'), '<svg viewBox="0 0 24 24" width="24" height="24" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round" class="css-i6dzq1"><polyline points="9 18 15 12 9 6"></polyline></svg>')
            route_menu_handler(route_index, 'next')


            break;
        case 2:
            btn_text($('#next'), '<svg viewBox="0 0 24 24" width="24" height="24" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round" class="css-i6dzq1"><polyline points="9 18 15 12 9 6"></polyline></svg>')
            route_menu_handler(route_index, 'next')
            $('#next').addClass('disabled')
            $('#wizard1-h-1').css('display', 'none')
            $('#wizard1-p-1').css('display', 'none')

            if ($('#method').val() === 'Админ панель') {
                $('#panel_add_p_3').css('display', 'block')
                $('#panel_add_h_3').css('display', 'block')

            } else {
                $('#excel_add_p_3').css('display', 'block')
                $('#excel_add_h_3').css('display', 'block')

            }

            break;

        default:
            break;
    }

}

let enabled_route_number = 0
// выбор проекта
$(".table-row").on('click', function (e) {
    $(".table-row").css('background-color', '').css('color', '').removeClass('company-chosen')
    $(this).css('background-color', '#6c5ffc').css('color', 'white').addClass('company-chosen')
    $('#next').removeClass('disabled')
})

$('#next').on('click', function () {
    if ($(this).hasClass('disabled')) {
        if (enabled_route_number === 1) {
            toastr.error('Выберите проект')
        }
    } else {
        $('.route-item').each(function (i, obj) {
            if (!$(this).hasClass('disabled')) {
                enabled_route_number = parseInt($(this).find('.number').html())

            }

        })
        $('#previous').removeClass('disabled')
        route_handler(enabled_route_number)

    }

})
$('#previous').on('click', function () {
    $('.route-item').each(function (i, obj) {
        if (!$(this).hasClass('disabled')) {
            enabled_route_number = parseInt($(this).find('.number').html())

        }

    })
    // $('#next').removeClass('disabled')
    switch (enabled_route_number) {
        case 2:
            $('.team-table').DataTable().clear().destroy()
            $('#wizard1-h-1').css('display', 'none')
            $('#wizard1-p-1').css('display', 'none')
            $('#wizard1-h-0').css('display', 'block')
            $('#wizard1-p-0').css('display', 'block')
            $(this).addClass('disabled')
            break;
        case 3:
            $('#wizard1-h-1').css('display', 'block')
            $('#wizard1-p-1').css('display', 'block')
            $('#panel_add_p_3').css('display', 'none')
            $('#panel_add_h_3').css('display', 'none')
            $('#excel_add_p_3').css('display', 'none')
            $('#excel_add_h_3').css('display', 'none')
            $('#next').removeClass('disabled').html('<svg viewBox="0 0 24 24" width="24" height="24" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round" class="css-i6dzq1"><polyline points="9 18 15 12 9 6"></polyline></svg>')
            break;
        default:
            break;
    }
    route_menu_handler(enabled_route_number, 'previous')

})

let table = ''

function process_table(element) {
    $(element).DataTable().destroy()
    $(element).DataTable({
        "searching": true,
        "destroy": true,
        "paging": true,
        "language": {
            "url": "//cdn.datatables.net/plug-ins/9dcbecd42ad/i18n/Russian.json"
        },
        "initComplete": function () {

        },
    })
}

$("#parse_file").on("click", function () {
    //Reference the FileUpload element.
    $('.error-message-close-btn').each(function (i, e) {
        e.click()
    })
    let fileUpload = $("#files")[0];

    //Validate whether File is valid Excel file.
    let regex = /^([а-яА-Яa-zA-Z0-9\s_\\.\-:])+(.xls|.xlsx)$/;
    if (regex.test(fileUpload.value.toLowerCase())) {
        if (typeof (FileReader) != "undefined") {
            let reader = new FileReader();

            //For Browsers other than IE.
            if (reader.readAsBinaryString) {
                reader.onload = function (e) {
                    ProcessExcel(e.target.result);
                };
                reader.readAsBinaryString(fileUpload.files[0]);
            } else {
                //For IE Browser.
                reader.onload = function (e) {
                    let data = "";
                    let bytes = new Uint8Array(e.target.result);
                    for (let i = 0; i < bytes.byteLength; i++) {
                        data += String.fromCharCode(bytes[i]);
                    }
                    ProcessExcel(data);
                };
                reader.readAsArrayBuffer(fileUpload.files[0]);
            }
        } else {
            toastr.error("Браузер не поддерживает HTML5.");
        }
    } else {
        show_error_message('Загрузите корректный файл')
    }
});

function ProcessExcel(data) {
    //Read the Excel File data.
    let workbook = XLSX.read(data, {
        type: 'binary'
    });

    //Fetch the name of First Sheet.
    let sheet_exists = false
    let sheets = workbook.SheetNames;
    let sheet
    for (let i = 0; i < sheets.length; i++) {
        if (sheets[i] === 'Данные участников') {
            sheet = sheets[i]
            sheet_exists = true
        }
    }

    // console.log(firstSheet)
    if (sheet_exists) {
        //Read all rows from First Sheet into an JSON array.
        let excelRows = XLSX.utils.sheet_to_row_object_array(workbook.Sheets[sheet]);
        let row_obj = excelRows[0]
        // console.log(row_obj)
        let error_exists = false
        let heads_ok = false
        let heads_after_check_ok = true
        let after_all_checks_ok = true
        let all_fields_filled_out = true
        let head_vals = {
            'array': [
                'Фамилия Имя (или псевдоним по выбору участника)',
                'E-mail для приглашений',
                'Роль',
                'Должность',
                'Индустрия',
                'Пол',
                'Год рождения'

            ]
        }
        let gender_vals = [
            'Мужской',
            'Женский',
        ]
        // let head_vals = [
        // ]


        // console.log(XLSX.utils.sheet_to_json(workbook.Sheets[sheet], {header:1})[0]);
        let sheet_header = XLSX.utils.sheet_to_json(workbook.Sheets[sheet], {header: 1})[0]
        for (let i = 0; i < sheet_header.length; i++) {
            heads_ok = false
            $.each(head_vals['array'], function (index, val) {
                if (sheet_header[i].trim() === val) {
                    heads_ok = true
                }
            })
            if (heads_ok === false) {
                heads_after_check_ok = false
                show_error_message(sheet_header[i] + ' - некорректное название столбца')
            }

        }
        if (heads_after_check_ok) {
            let employees_obj = []
            let data_errors_exists = true
            for (let i = 0; i < excelRows.length; i++) {
                // all_fields_filled_out = true
                // проверка полей на пустоту

                all_fields_filled_out = allFieldsFilledOut(excelRows[i], i + 2)

                if (all_fields_filled_out) {


                    let row_to_add = {}
                    $.each(excelRows[i], function (key, val) {
                        data_errors_exists = true
                        switch (key) {
                            case 'Фамилия Имя (или псевдоним по выбору участника)':
                                row_to_add[key] = val
                                break;
                            case 'E-mail для приглашений':
                                if (isEmail(val)) {
                                    row_to_add[key] = val
                                } else {
                                    after_all_checks_ok = false
                                    data_errors_exists = true
                                    show_error_message('Указан некорректный Email (строка - ' + (i + 2) + ')')
                                }
                                break;
                            case 'Роль':
                                $.each(employee_roles_obj['array'], function (index, v) {
                                    if (val === v) {
                                        row_to_add[key] = val
                                        data_errors_exists = false
                                    }
                                })
                                if (data_errors_exists) {
                                    after_all_checks_ok = false
                                    show_error_message('Роль отсутствует в базе данных (строка - ' + (i + 2) + ')')
                                }

                                break;
                            case 'Должность':
                                $.each(employee_positions_obj['array'], function (index, v) {
                                    if (val === v) {
                                        row_to_add[key] = val
                                        data_errors_exists = false
                                    }
                                })
                                if (data_errors_exists) {
                                    after_all_checks_ok = false
                                    show_error_message('Должность отсутствует в базе данных (строка - ' + (i + 2) + ')')
                                }
                                break;
                            case 'Индустрия':
                                $.each(industries_obj['array'], function (index, v) {
                                    if (val === v) {
                                        row_to_add[key] = val
                                        data_errors_exists = false
                                    }
                                })
                                if (data_errors_exists) {
                                    after_all_checks_ok = false
                                    show_error_message('Индустрия отсутствует в базе данных (строка - ' + (i + 2) + ')')
                                }
                                break;
                            case 'Пол':
                                $.each(genders_obj['array'], function (index, v) {
                                    if (val === v) {
                                        row_to_add[key] = val
                                        data_errors_exists = false
                                    }
                                })

                                // for(let i=0; i < gender_vals.length; i++){
                                //     console.log(gender_vals[i])
                                //     if(val === gender_vals[i]){
                                //         row_to_add[key] = val
                                //         data_errors_exists = false
                                //     }
                                //
                                // }
                                if (data_errors_exists) {
                                    after_all_checks_ok = false
                                    show_error_message('Пол отсутствует в базе данных (строка - ' + (i + 2) + ')')
                                }

                                break;
                            case 'Год рождения':
                                if (isYear(val)) {
                                    row_to_add[key] = val
                                } else {
                                    after_all_checks_ok = false
                                    data_errors_exists = true
                                    show_error_message('Указан некорректный Год рождения (строка - ' + (i + 2) + ')')
                                }
                                break;
                            default:
                                break;
                        }

                    })


                    employees_obj.push(row_to_add)

                }
            }
            if (after_all_checks_ok && all_fields_filled_out) {
                console.log(employees_obj)
                btn_spinner($('#parse_file'))
                $.ajax({
                    headers: {"X-CSRFToken": token},
                    url: url_save_new_employee_xls,
                    type: 'POST',
                    data: JSON.stringify({
                        'employees': employees_obj,
                        'company_id': $('.company-chosen').attr('id').split('_')[2]
                    }),
                    processData: false,
                    contentType: false,
                    error: function (data) {
                        toastr.error('Ошибка', data)
                    },
                    success: function (data) {
                        console.log(data)
                        let data_json = data['emails']
                        let cnt = data['cnt']
                        let cnt_html_emails = '<div style="text-align: left; padding-left: 7px;">' +
                            '<hr class="solid mt-0" style="background-color: black;">' +
                            '<b>Количество добавленных сотрудников - ' + cnt + '</b>' +
                            '</div>'
                        let cnt_html_no_emails = '<div style="text-align: center">' +
                            '<hr class="solid mt-0" style="background-color: black;">' +
                            '<b>Количество добавленных сотрудников - ' + cnt + '</b>' +
                            '</div>'
                        let output_html = ''
                        console.log(data_json)
                        if (data_json !== 'None') {
                            let list_html = '<ul><hr class="solid" style="background-color: black;">'
                            for (let i = 0; i < data_json.length; i++) {
                                list_html += '<li style="text-align: left; padding-left: 7px;"><b>'
                                list_html += '- ' + data_json[i]
                                list_html += '</b></li>'
                            }
                            list_html += '</ul>'
                            output_html = '<div>Сотрудники со следующими email уже существуют в базе данных:' +
                                list_html +
                                '</div>' +
                                '<br>' + cnt_html_emails
                            Swal.fire({
                                // title: 'Сотрудники добавлены',
                                html: output_html,
                                icon: 'warning',
                                confirmButtonColor: '#3085d6',
                                cancelButtonColor: '#d33',
                                confirmButtonText: 'ОК'
                            }).then((result) => {
                                if (result.isConfirmed) {
                                    // window.location.href = url_panel_home
                                }
                            })

                        } else {
                            output_html = '<div>Сотрудники добавлены в базу данных' + '</div>' +
                                '<br>' + cnt_html_no_emails
                            Swal.fire({
                                html: output_html,
                                icon: 'success',
                                confirmButtonColor: '#3085d6',
                                cancelButtonColor: '#d33',
                                confirmButtonText: 'ОК'
                            }).then((result) => {
                                if (result.isConfirmed) {
                                    // window.location.href = url_panel_home
                                }
                            })

                        }
                        btn_text($('#parse_file'), 'Загрузить')
                    }
                });
            }

        }
    } else {
        show_error_message('Необходимый лист в файле осутствует')
    }
}

// $('#parse_file').on('click', handleFileSelect(document.getElementById('files')))

function show_error_message(text) {
    let html_template = $('#template_error_block').html()
    let html_block = html_template.replace('message_text', text)
    // $('.error_message').text(text)
    $('#error_block').append(html_block)
}


function isYear(year) {
    let regex = /^\d\d\d\d$/g
    return regex.test(year);
}

function allFieldsFilledOut(obj, column_number) {
    let fields_not_empy = true
    if (!('E-mail для приглашений' in obj)) {
        fields_not_empy = false
        show_error_message('Поле "E-mail для приглашений" пустое (строка - ' + column_number + ')')
    }
    if (!('Роль' in obj)) {
        fields_not_empy = false
        show_error_message('Поле "Роль" пустое (строка - ' + column_number + ')')
    }
    if (!('Должность' in obj)) {
        fields_not_empy = false
        show_error_message('Поле "Должность" пустое (строка - ' + column_number + ')')
    }

    if (!('Индустрия' in obj)) {
        fields_not_empy = false
        show_error_message('Поле "Индустрия" пустое (строка - ' + column_number + ')')
    }

    if (!('Пол' in obj)) {
        fields_not_empy = false
        show_error_message('Поле "Пол" пустое (строка - ' + column_number + ')')
    }

    if (!('Год рождения' in obj)) {
        fields_not_empy = false
        show_error_message('Поле "Год рождения" пустое (строка - ' + column_number + ')')
    }

    return fields_not_empy
}

$('#save_employee').on('click', function () {
    let name = $('#employee_name').val()
    let email = $('#employee_email').val()
    let role = $('#employee_role').val()
    let position = $('#employee_position').val()
    let industry = $('#employee_industry').val()
    let gender = $('#employee_gender').val()
    let employee_birth_year = $('#employee_birth_year').val()
    let test_ok = true

    $('#employee_email').on('click', function () {
        $('#employee_email').removeClass('is-invalid')
    })
    $('#employee_name').on('click', function () {
        $('#employee_name').removeClass('is-invalid')
    })
    if (email === '') {
        $('#employee_email').addClass('is-invalid')
        test_ok = false
    } else {
        if (!isEmail(email)) {
            toastr.error('Указан некорректный email')
            test_ok = false
        }
    }
    if (name === '') {
        test_ok = false
        $('#employee_name').addClass('is-invalid')
    }

    if (!test_ok) {
        toastr.error('Имя и Email должны быть заполнены')
    }else {
        btn_spinner($('#save_employee'))
        let role_id = $('#employee_role option:selected').val().split('_')[2]
        let position_id = $('#employee_position option:selected').val().split('_')[2]
        let industry_id = $('#employee_industry option:selected').val().split('_')[2]
        let gender_id = $('#employee_gender option:selected').val().split('_')[2]

        let data = {
            'name': name,
            'role_id': role_id,
            'email': email,
            'position_id': position_id,
            'industry_id': industry_id,
            'gender_id': gender_id,
            'employee_birth_year': employee_birth_year
        }
        console.log(data)
        $.ajax({
            headers: {"X-CSRFToken": token},
            url: url_save_new_employee_html,
            type: 'POST',
            data: JSON.stringify({
                'employee_data': data,
                'company_id': $('.company-chosen').attr('id').split('_')[2]
            }),
            processData: false,
            contentType: false,
            error: function (data) {
                toastr.error('Ошибка', data)
            },
            success: function (data) {
                console.log(data)
                let output_html
                if (data === 'email exists') {
                    output_html = '<hr class="solid mt-0" style="background-color: black;">' +
                        '<div>Сотрудник с указанным email уже существует в базе данных</div>' +
                        '<br>' +
                        '<hr class="solid mt-0" style="background-color: black;">'
                    Swal.fire({
                        html: output_html,
                        icon: 'warning',
                        confirmButtonColor: '#3085d6',
                        cancelButtonColor: '#d33',
                        confirmButtonText: 'ОК'
                    }).then((result) => {
                        if (result.isConfirmed) {
                            //window.location.href = url_panel_home
                        }
                    })

                } else {
                    let output_html = '<h2 class="mb-0" style="text-align: center">Данные сохранены</h2>' +
                        '<br>' +
                        '<hr class="solid mt-0" style="background-color: black;">' +
                        '<h4 style="text-align: center">Cотрудник добавлен в базу данных</h4>' +
                        '<hr class="solid mt-0" style="background-color: black;">'

                    Swal.fire({
                        html: output_html,
                        icon: 'success',
                        confirmButtonColor: '#3085d6',
                        cancelButtonColor: '#d33',
                        confirmButtonText: 'ОК'
                    }).then((result) => {
                        if (result.isConfirmed) {
                            window.location.reload()
                        }
                    })

                }

                btn_text($('#save_employee'), 'Загрузить')
            }
        });

    }

})
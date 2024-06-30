let errors_arr = []
let all_rows_filled_out = true
let questionnaire_results_arr = []

let head_vals = {
    'array': [
        'Компания',
        'ФИО',
        'Email',
        'Пол',
        'Должности',
        'Индустрии',
        'Роли/Функции сотрудников',
        'Год рождения',
        'Заполнение',
        'Дата заполнения',
        '1_1',
        '1_10',
        '1_11',
        '1_12',
        '1_13',
        '1_14',
        '1_15',
        '1_2',
        '1_3',
        '1_4',
        '1_5',
        '1_6',
        '1_7',
        '1_8',
        '1_9',
        '2_10',
        '2_12',
        '2_14',
        '2_15',
        '2_16',
        '2_17',
        '2_18',
        '2_19',
        '2_2',
        '2_20',
        '2_8',
        '3_13',
        '3_14',
        '3_15',
        '3_16',
        '3_17',
        '3_18',
        '4_1',
        '4_10',
        '4_2',
        '4_3',
        '4_4',
        '4_5',
        '4_6',
        '4_7',
        '4_8',
        '4_9',
        '1_100',

    ]
}


$("#parse_questionnaire_results_file").on("click", function () {
    //Reference the FileUpload element.
    all_rows_filled_out = true
    $('.error-message-close-btn').each(function (i, e) {
        e.click()
    })

    errors_arr = []

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
        toastr.error('Загрузите корректный файл')
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
    // if (sheet_exists) {
    //Read all rows from First Sheet into an JSON array.
    let excelRows = XLSX.utils.sheet_to_row_object_array(workbook.Sheets[sheets[0]]);
    let row_obj = excelRows[0]
    // console.log(row_obj)
    let error_exists = false
    let heads_ok = false
    let heads_after_check_ok = true
    let after_all_checks_ok = true
    let all_fields_filled_out = true
    let gender_vals = [
        'Мужской',
        'Женский',
    ]
    // let head_vals = [
    // ]


    // console.log(XLSX.utils.sheet_to_json(workbook.Sheets[sheet], {header:1})[0]);
    let sheet_header = XLSX.utils.sheet_to_json(workbook.Sheets[sheets[0]], {header: 1})[0]
    console.log(sheet_header)
    for (let i = 0; i < sheet_header.length; i++) {
        heads_ok = false
        $.each(head_vals['array'], function (index, val) {
            if (sheet_header[i].trim() === val) {
                heads_ok = true
            }
        })
        if (heads_ok === false) {
            heads_after_check_ok = false
            toastr.error(sheet_header[i] + ' - некорректное название столбца')
            errors_arr.push(sheet_header[i] + ' - некорректное название столбца')
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

            if (!all_fields_filled_out) {


                let row_to_add = {}
                row_to_add['categories'] = []
                $.each(excelRows[i], function (key, vl) {
                    // console.log(`key - ${key} val - ${val}`)
                    let val = vl.trim()
                    data_errors_exists = true
                    switch (key) {
                        case 'Дата заполнения':
                            row_to_add[key] = val
                            break;
                        case 'Заполнение':
                            row_to_add[key] = val
                            break;
                        case 'Компания':
                            row_to_add[key] = val
                            break;
                        case 'ФИО':
                            row_to_add[key] = val
                            break;
                        case 'Email':
                            if (isEmail(val)) {
                                row_to_add[key] = val
                            } else {
                                after_all_checks_ok = false
                                data_errors_exists = true
                                errors_arr.push('Указан некорректный Email ' + val + '(строка - ' + (i + 2) + ')')
                                // show_error_message('Указан некорректный Email (строка - ' + (i + 2) + ')')
                            }
                            break;
                        case 'Роли/Функции сотрудников':
                            $.each(employee_roles_obj['array'], function (index, v) {
                                // console.log(`val - "${val}" v - "${v}"`)
                                if (val === v.replace(/&amp;/g, '&')) {
                                    row_to_add[key] = val
                                    data_errors_exists = false
                                }
                            })
                            if (data_errors_exists) {
                                after_all_checks_ok = false
                                errors_arr.push('Роль/Функция "' + val + '" отсутствует в базе данных (строка - ' + (i + 2) + ')')
                                // show_error_message('Роль отсутствует в базе данных (строка - ' + (i + 2) + ')')
                            }

                            break;
                        case 'Должности':
                            $.each(employee_positions_obj['array'], function (index, v) {
                                if (val === v.replace(/&amp;/g, '&')) {
                                    row_to_add[key] = val
                                    data_errors_exists = false
                                }
                            })
                            if (data_errors_exists) {
                                after_all_checks_ok = false
                                errors_arr.push('Должность "' + val + '" отсутствует в базе данных (строка - ' + (i + 2) + ')')
                                // show_error_message('Должность отсутствует в базе данных (строка - ' + (i + 2) + ')')
                            }
                            break;
                        case 'Индустрии':
                            $.each(industries_obj['array'], function (index, v) {
                                if (val === v.replace(/&amp;/g, '&')) {
                                    row_to_add[key] = val
                                    data_errors_exists = false
                                }
                            })
                            if (data_errors_exists) {
                                after_all_checks_ok = false
                                errors_arr.push('Индустрия "' + val + '" отсутствует в базе данных (строка - ' + (i + 2) + ')')
                                // show_error_message('Индустрия отсутствует в базе данных (строка - ' + (i + 2) + ')')
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
                                errors_arr.push('Пол "' + val + '" отсутствует в базе данных (строка - ' + (i + 2) + ')')
                                // show_error_message('Пол отсутствует в базе данных (строка - ' + (i + 2) + ')')
                            }

                            break;
                        case 'Год рождения':
                            if (isYear(val)) {
                                row_to_add[key] = val
                            } else {
                                after_all_checks_ok = false
                                data_errors_exists = true
                                errors_arr.push('Указан некорректный Год рождения (строка - ' + (i + 2) + ')')
                                // show_error_message('Указан некорректный Год рождения (строка - ' + (i + 2) + ')')
                            }
                            break;
                        default:
                            // if(key !== 'Заполнение'){
                            //
                            // }
                            $.each(categories_obj['array'], function (index, v) {
                                if (key === v || key === 'Заполнение') {
                                    data_errors_exists = false
                                }
                            })
                            if (data_errors_exists) {
                                after_all_checks_ok = false
                                errors_arr.push('Код шкалы "' + key + '" отсутствует в базе данных (строка - ' + (i + 2) + ')')
                                // show_error_message('Индустрия отсутствует в базе данных (строка - ' + (i + 2) + ')')
                            } else {
                                if (val < 0 || val > 10) {
                                    errors_arr.push('Очки указаны неверно (код - ' + key + '; строка - ' + (i + 2) + ')')

                                } else {
                                    // row_to_add[key] = val
                                    if (key !== 'Заполнение') {
                                        let category_obj = {}
                                        category_obj[key] = val
                                        row_to_add['categories'].push(category_obj)

                                    }
                                }

                            }


                            break;
                    }
                })


                questionnaire_results_arr.push(row_to_add)

            }
            //
        }
        if (after_all_checks_ok && all_rows_filled_out) {
            console.log(employees_obj)
            btn_spinner($('#parse_questionnaire_results_file'))
            $.ajax({
                headers: {"X-CSRFToken": token},
                url: url_save_report_data_from_xls,
                type: 'POST',
                data: JSON.stringify({
                    'questionnaire_results_arr': questionnaire_results_arr,
                }),
                processData: false,
                contentType: false,
                error: function (data) {
                    toastr.error('Ошибка', data)
                },
                success: function (data) {
                    btn_text($('#parse_questionnaire_results_file'), 'Загрузить')
                    toastr.success('Данные сохранены')
                }
            });
        } else {
            $('#modal_errors_body').html('')
            errors_arr.forEach(function (item) {
                $('#modal_errors_body').append('<div>' + item + '</div>')

            })
            $('#modal_errors').modal('show')
        }

    }
    // } else {
    //     show_error_message('Необходимый лист в файле осутствует')
    // }

    console.log(errors_arr)
    console.log(questionnaire_results_arr)

}

function show_error_message(text) {
    let html_template = $('#template_error_block').html()
    let html_block = html_template.replace('message_text', text)
    // $('.error_message').text(text)
    $('#error_block').append(html_block)
}

function allFieldsFilledOut(obj, row_number) {
    let fields_not_empty = false
    let field_empty = false

    head_vals['array'].forEach(function (head_val) {
        if (!(head_val in obj)) {
            field_empty = true
            errors_arr.push('Поле "' + head_val + '" пустое (строка - ' + row_number + ')')
        }

    })

    if (field_empty) {
        all_rows_filled_out = false
    }
    return fields_not_empty
}

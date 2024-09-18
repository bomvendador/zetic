let group_color
let group_color_picker_element
let participants_with_report_array = []

function coloris(element) {
    Coloris({
        themeMode: 'dark',
        alpha: false,
        wrap: true,
        swatches: [
            'rgb(255,255,0)',
            'rgb(255,0,0)',
            'rgb(102,178,255)',
            'rgb(0,0,255)',
            'rgb(255,51,255)',
            'rgb(127,0,255)',
            'rgb(102,255,178)',
            'rgb(0,153,0)',
        ],
        // {#parent: element#}
    });

}

$(document).ready(function () {
    // console.log('ready');

    $('#tbody_undistributed_participants .category-selected').each(function () {
        $(this).attr('title', $(this).find('option:selected').text())
    })
})

let participants_numbers_used = []
let participant_email_for_number = ''

$('#tbody_undistributed_participants').on('click', '.add-participant-number', function () {
    participants_numbers_used = []
    participant_email_for_number = $(this).closest('tr').find('.email').eq(0).text()
    // console.log(participant_email_for_number)
    let numbers_user_str = ''
    let cnt = 0
    $('#tbody_undistributed_participants .participant-number').each(function () {
        if ($(this).closest('tr').find('.email').eq(0).text() !== participant_email_for_number) {
            let participant_number = $(this).find('span').text()
            participants_numbers_used.push(participant_number)
            if (participant_number !== "") {
                if (cnt === 0) {
                    numbers_user_str = $(this).find('span').text()
                } else {
                    numbers_user_str += ', ' + $(this).find('span').text()
                }
                cnt += 1

            }

        }

    })
    $('#participant_number_not_available').html(numbers_user_str)
    $('#modal_participant_number').modal('show')
})

$('#modal_save_participant_number').on('click', function () {
    let participant_number_entered = $('#modal_input_participant_number').val()
    let entered_used_number = false;
    participants_numbers_used.forEach(function (num) {
        if (num === participant_number_entered) {
            entered_used_number = true
        }
    })
    if (participant_number_entered === '' || isNaN(participant_number_entered) || entered_used_number) {
        toastr.error('Введено некорректное число')
    } else {
        $('#tbody_undistributed_participants tr').each(function () {
            let email = $(this).find('td').eq(3).text()
            if (email === participant_email_for_number) {
                $(this).find('.participant-number').eq(0).html(`<span>${participant_number_entered}</span>`)
                $(this).find('.participant-number').css('background-color', '#bdbdbd').css('cursor', 'pointer')
                $(this).find('.participant-number').addClass('add-participant-number')
            }
        })
        $('#modal_participant_number').modal('hide')
    }
})


$('#tbody_undistributed_participants').on('change', '.category-selected', function () {
    $(this).attr('title', $(this).find('option:selected').text())
})

$('#tbody_undistributed_participants').on('click', '.add-participant-number', function () {
    $(this).attr('title', $(this).find('option:selected').text())
})

$('#tbody_undistributed_participants').on('click', '.delete-participant-from-group-report', function () {

    let output_html = '<h2 class="mb-0" style="text-align: center">Удаление сотрудника из отчета</h2>' +
        '<br>' +
        '<hr class="solid mt-0" style="background-color: black;">' +
        '<h4 style="text-align: center">Удалить сотрудника?</h4>' +
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
            let tr = $(this).closest('tr')
            let data_participant_number = tr.data('participant-number')
            if (data_participant_number !== '') {
                let employee_id = $(this).closest('tr').data('employee-id')
                show_progressbar_loader()
                $.ajax({
                    headers: {"X-CSRFToken": token},
                    url: url_delete_participant_from_group_report,
                    type: 'POST',
                    data: JSON.stringify({
                        'employee_id': employee_id,
                        'group_report_id': group_report_id
                    }),
                    processData: false,
                    contentType: false,
                    error: function (data) {
                        toastr.error('Ошибка', data)
                    },
                    success: function (data) {
                        hide_progressbar_loader()
                        tr.remove()

                    }
                });


            } else {
                $(this).closest('tr').remove()
            }
        }
    })


})

$('#create_group_report').on('click', function () {
    let output_html = '<h2 class="mb-0" style="text-align: center">Комментарии к отчету</h2>' +
        '<br>' +
        '<hr class="solid mt-0" style="background-color: black;">' +
        '<h4 style="text-align: center">Добавить комментарии к отчету?</h4>' +
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
            $('#input-modal-report-comments').modal('show')
        } else {
            save_report()
        }
    })

})


$('#add_participants_from_modal').on('click', function () {
    let participants_chosen_cnt = 0
    $('#participants_to_add_table .participant-chosen').each(function () {
        if ($(this).prop('checked')) {
            participants_chosen_cnt = participants_chosen_cnt + 1
            let email_from_modal = $(this).closest('tr').find('td').eq(2).text()
            // console.log(participants_with_report_array)
            participants_with_report_array.forEach(function (item) {
                let participant_data = item['participant_data'][0]
                let participant_squares = participant_data['participant_squares']

                let squares_data = item['squares_data']
                if (email_from_modal === participant_data['email']) {

                    // console.log(participant_data)
                    // console.log(participant_data['participant_squares'])
                    let html = ''

                    html = '<tr class="table-row-undistributed-participant" style = "" data-participant-number="">' +
                        '<td class="bold-participant" style="text-align: center;vertical-align: middle;" >' +
                        '<input class="checkbox-custom" style="width: 16px; height: 16px" type="checkbox" name="" value="0">' +
                        '</td>' +
                        '<td class="participant-group" style="text-align: center;vertical-align: middle">' +
                        '<input class="checkbox-custom" style="width: 16px; height: 16px" type="checkbox" name="" value="0">' +
                        '</td><td class="fio" style="vertical-align: middle">' + participant_data["fio"] + '</td>' +
                        '<td class="email" style="vertical-align: middle">' + participant_data["email"] + '</td>' +
                        '<td class="role_name" style="vertical-align: middle">' + participant_data["role_name"] + '</td>' +
                        '<td class="position" style="vertical-align: middle">' + participant_data["position"] + '</td>' +
                        '<td style="vertical-align: middle">'
                    if (participant_squares.length > 0) {
                        participant_squares.forEach(function (square) {
                            html += '<div>' + square["square_code"] + ' - ' + square["square_name"] + ' (' + square["percentage"] + '%)</div>'
                        })
                    } else {
                        html += 'Отсутствует'
                    }
                    html += '</td>' +
                        '<td>' +
                        '<select name="category" class="form-control form-select category-selected" data-bs-placeholder="Выберите категорию">' +
                        '<option value=""></option>'
                    squares_data.forEach(function (square) {
                        html += '<option value="' + square["square_role_name"] + '">' + square["code"] + ' - ' + square["square_name"] + ' - ' + square["square_role_name"] + '</option>'
                    })
                    html += '</select>' +
                        '</td>' +
                        '<td class="participant-number" style="vertical-align: middle; text-align: center">' +
                        '<button class="btn btn-primary my-1 cursor-pointer col-12 add-participant-number" type="button">+</button>' +
                        '</td>' +
                        '<td style="vertical-align: middle; text-align: center">' +
                        '<button class="btn-close delete-participant-from-group-report" aria-label="Close">' +
                        '<span aria-hidden="true">×</span>' +
                        '</button>' +
                        '</td>'

                    '</tr>'

                    $('#tbody_undistributed_participants').append(html)
                    $('#edit_group_report_add_participants_modal').modal('hide')

                }
            })
        }
    })
    if (participants_chosen_cnt === 0) {
        toastr.error('Сотрудники не выюраны')
    }
})


$('#open_modal_for_adding_participants').on('click', function () {
    show_progressbar_loader()
    participants_with_report_array = []
    $.ajax({
        headers: {"X-CSRFToken": token},
        url: url_get_available_participants_for_group_report,
        type: 'POST',

        data: JSON.stringify({
            'company_id': company_id,
            'group_report_id': group_report_id,
        }),
        processData: false,
        contentType: false,
        error: function (data) {
            toastr.error('Ошибка', data)
        },
        success: function (data) {
            let html = '';
            let participants_could_be_added_cnt = 0
            participants_with_report_array = data
            hide_progressbar_loader()
            data.forEach(function (item) {
                let participant_data = item['participant_data'][0];
                // console.log(participant_data)
                let participant_already_is_in_table = false

                $('#tbody_undistributed_participants tr').each(function () {
                    let email = $(this).find('td').eq(3).text()
                    if (participant_data["email"] === email) {
                        participant_already_is_in_table = true
                    }

                })

                if (!participant_already_is_in_table) {
                    participants_could_be_added_cnt += 1
                    html = html + '<tr class="table-row-participant-to-add-to-group-report" style = "" data-participant-number = "">' +
                        '<td class="" style = "" >' +
                        // '<td class="" style = "text-align: center;vertical-align: middle;" >' +
                        '<input class="checkbox-custom participant-chosen" style = "width: 16px; height: 16px" type = "checkbox" name = "" value = "0">' +
                        '</td>' +
                        '<td class="fio" style="vertical-align: middle">' + participant_data["fio"] + '</td>' +
                        '<td class="email" style="vertical-align: middle">' + participant_data["email"] + '</td>' +
                        '<td class="role_name" style="vertical-align: middle">' + participant_data["role_name"] + '</td>' +
                        '<td class="position" style="vertical-align: middle">' + participant_data["position"] + '</td>' +
                        '</tr>'
                }


            })
            if (participants_could_be_added_cnt > 0) {
                $('#participants_to_add_table').DataTable().clear().destroy()
                $('#participants_to_add_table tbody').html(html)
                process_table('#participants_to_add_table')

                $('#edit_group_report_add_participants_modal').modal('show')

            } else {
                toastr.warning('Все участники уже добавлены')
            }

        }
    });


})

$('#check_all_participants_for_group_report').on('click', function () {
    // console.log($('#check_all_participants_for_group_report').prop('checked'))
    $('#participants_to_add_table .participant-chosen').each(function () {
        // console.log('ddd')
        if ($('#check_all_participants_for_group_report').prop('checked')) {
            $(this).prop('checked', true)
        } else {
            $(this).prop('checked', false)
        }
    })
})


document.addEventListener('coloris:pick', event => {
    group_color = event.detail.color
    $(group_color_picker_element).css('background', event.detail.color).css('border', 'solid')
});

$('#distribution_participants_groups_modal').on('click', '.group-color-picker', function () {
    group_color_picker_element = this
})


$('#main-container').on('click', '.checkbox-custom', function () {
    if ($(this).val() === '0') {
        set_checkbox_checked(this)
    } else {
        set_checkbox_unchecked(this)
    }
})

$('#distribution_participants_groups_modal').on('click', '.radio-custom', function () {
    $('#distribution_participants_groups_modal').find('.radio-custom').each(function () {
        set_checkbox_unchecked(this)
    })
    set_checkbox_checked(this)
})

$('#add_participants_group').on('click', function () {
    let groups_qnt = $('#participants_groups_table tbody tr').length
    let last_group_val = $('#participants_groups_table tbody tr:last-child td:nth-child(2) input').val()
    let tr_html = '<tr class="participants-group-modal-item" style="vertical-align: middle">' +
        '<td style="vertical-align: middle"><input class="radio-custom" style="width: 16px; height: 16px" type="radio" name="" value="0"></td>' +
        '<td><input type="text group-name" class="form-control" value=""></td>' +
        '<td style="vertical-align: middle">' +
        '<div class="media-body">' +
        '<input class="cursor-pointer group-color-picker" type="text" data-coloris style="width: 30px; color: transparent; background-color: rgb(255,255,0);border: solid" value="rgb(255,255,0)"/>' +
        '<span class="d-block w-80p">' +
        '<span class="color-picker"></span>' +
        '</span>' +
        '</div>' +
        '</td>' +
        '<td style="vertical-align: middle"><i class="fa fa-times delete-group cursor-pointer" aria-hidden="true" style="font-size: 20px"></i></td>' +
        '</tr>'
    if (groups_qnt === 0) {
        let element = $('#participants_groups_table tbody').append(tr_html)
        // console.log(element)
        coloris(element)
    } else {
        if (last_group_val !== '') {
            let element = $('#participants_groups_table tbody').append(tr_html)
            coloris(element)
        } else {
            toastr.error('Введите название группы')
        }

    }
    set_checkbox_unchecked($('#participants_groups_table tbody tr td:nth-child(1) input'))
    set_checkbox_checked($('#participants_groups_table tbody tr:last-child td:nth-child(1) input'))


})


$('#distribution_participants_groups_modal').on('click', '.delete-group', function () {
    $(this).closest('tr').remove()
})

$('#participants_groups').on('click', function () {
    let participants_chosen_for_group = $('#tbody_undistributed_participants tr td:nth-child(2) input[value=1]').length
    // console.log('participants_chosen_for_group - ' + participants_chosen_for_group)
    if (participants_chosen_for_group == 0) {
        $('#set_groups_to_participants').hide()
        // console.log('hide')
    } else {
        $('#set_groups_to_participants').show()
        // console.log('show')
    }
    $('#distribution_participants_groups_modal').modal('show')
})

$('#set_groups_to_participants').on('click', function () {
    let groups_chosen = $('#participants_groups_table tbody tr td:nth-child(1) input[value=1]').length
    if (groups_chosen === 0) {
        toastr.error('Выберите группу')
    } else {
        let group_name = $('#participants_groups_table tbody tr td:nth-child(1) input[value=1]').closest('tr').find('td:nth-child(2) input').val()
        if (group_name === '') {
            toastr.error('Введите название группы')
        } else {
            let group_color = $('#participants_groups_table tbody tr td:nth-child(1) input[value=1]').closest('tr').find('td:nth-child(3) input').css('background-color')
            $('#tbody_undistributed_participants tr td:nth-child(2) input[value=1]').each(function () {
                $(this).closest('td').css('background-color', group_color).html('<span>' + group_name + '</span> <i class="fa fa-times cursor-pointer delete-participant-group" aria-hidden="true" style="margin-left: 5px"></i>')
            })
            $('#distribution_participants_groups_modal').modal('hide')
        }
    }
})


$('#select_all_for_group').on('click', function () {
    // console.log($(this).is(':checked'))
    let is_checked = $(this).is(':checked')
    $('#main-container .select-for-group-checkbox').each(function () {
        if (is_checked) {
            set_checkbox_checked(this)

        } else {
            set_checkbox_unchecked(this)
        }
    })
})


$('#undistributed-participants-table').on('click', '.delete-participant-group', function () {
    $(this).closest('td').css('background-color', 'white').html('<input class="checkbox-custom select-for-group-checkbox" style="width: 16px; height: 16px" type="checkbox" name="" value="0">')
})


let kernel1 = 0
let kernel2 = 0
$('#slider1_val').ionRangeSlider({
    min: 0,
    max: 10,
    step: 1,
    from: 4
});
$('#slider2_val').ionRangeSlider({
    min: 0,
    max: 10,
    step: 1,
    from: 6,
    onFinish: function (data) {
        kernel1 = data.from
        // console.log(kernel1)
    }
});
$('#slider3_val').ionRangeSlider({
    min: 0,
    max: 10,
    step: 1,
    from: 8,
    onFinish: function (data) {
        kernel2 = data.from
        // console.log(kernel2)
    }
});

$('.slider1').find('.irs-bar').attr('style', 'background: rgb(34, 170, 245)!important')
$('.slider1').find('.irs-slider.single').attr('style', 'background: rgb(34, 170, 245)!important')
$('.slider1').find('.irs-single').attr('style', 'background: rgb(34, 170, 245)!important')
$('.slider1').find('.irs-bar-edge').attr('style', 'background: rgb(0, 98, 153)!important')


$('#edit-individual-reports').on('click', function () {
    $('#scrollingmodal_participant_data').modal('show')
})

function route_menu_handler(route_index, btn_type) {
    let new_menu_number = 0
    if (btn_type === 'next') {
        new_menu_number = route_index + 1
    } else {
        new_menu_number = route_index - 1
    }
    // {#console.log('new_menu_number - ' + new_menu_number)#}
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
        if (new_menu_number === 3) {
            // {#$('#next').addClass('disabled')#}
            // {#$('#next').removeClass('cursor-pointer')#}
        } else {
            $('#next').removeClass('disabled')
            // {#$('#next').addClass('cursor-pointer')#}

        }

    } else {
        toastr.info('Конец')

    }
}

//пороговое значение соответствия правилам для ручного распределения
let min_rules_for_exception = 2

let project_name = company_name;

let square_names_obj = {
    '1_1': 'Магнит',
    '1_2': 'Фасилитатор',
    '1_3': 'Переговорщик',
    '1_4': 'Коннектор',
    '2_1': 'Визионер',
    '2_2': 'Авантюрист',
    '2_3': 'Искатель ресурсов',
    '2_4': 'Изобретатель',
    '3_1': 'Хранитель',
    '3_2': 'Вдохновитель',
    '3_3': 'Контролер',
    '3_4': 'Благородный служитель',
    '4_1': 'Организатор',
    '4_2': 'Любитель улучшений',
    '4_3': 'Реализатор',
    '4_4': 'Решатель проблем',
}

let code_name =
    {
        "1_1": "Шкала C ",
        "1_2": "Шкала O",
        "1_3": "Шкала Q4",
        "1_4": "Шкала F",
        "1_5": "Шкала N",
        "1_6": "Шкала I",
        "1_7": "Шкала А",
        "1_8": "Шкала M",
        "1_9": "Шкала Q2",
        "1_10": "Шкала G",
        "1_11": "Шкала Q3",
        "1_12": "Шкала Q1",
        "1_13": "Шкала L",
        "1_14": "Шкала H",
        "1_15": "Шкала E",
        "2_1": "Самообладание",
        "2_2": "Контроль над ситуацией",
        "2_3": "Позитивная самомотивация",
        "2_4": "Снижение значения стрессовой ситуации",
        "2_5": "Самоутверждение",
        "2_6": "Отвлечение",
        "2_7": "Бегство от стрессовой ситуации ",
        "2_8": "Антиципирующее избегание ",
        "2_9": "Замещение",
        "2_10": "Поиск социальной поддержки",
        "2_11": "Жалость к себе ",
        "2_12": "Социальная замкнутость",
        "2_13": "Самообвинение ",
        "2_14": "Заезженная пластинка",
        "2_15": "Самооправдание",
        "2_16": "Агрессия",
        "4_1": "Причастность ",
        "4_2": "Традиции",
        "4_3": "Жажда впечатлений",
        "4_4": "Эстетичность ",
        "4_5": "Гедонизм",
        "4_6": "Признание",
        "4_7": "Достижения ",
        "4_8": "Коммерческий подход",
        "4_9": "Безопасность ",
        "4_10": "Интеллект"
    }

let rule_1_1 = [
    ['1_7', 6, 10],
    ['1_6', 6, 10],
    ['1_5', 5, 10],
    ['1_8', 1, 5],
    ['4_1', 5, 10],
    ['4_3', 5, 10],
    ['4_4', 5, 10],
]

let rule_1_2 = [
    ['1_7', 6, 10],
    ['1_6', 6, 10],
    ['1_4', 5, 10],
    ['1_8', 5, 10],
    ['1_12', 5, 10],
    ['4_1', 5, 10],
    ['4_4', 5, 10],
    ['4_10', 5, 10],
]

let rule_1_3 = [
    ['1_7', 6, 10],
    ['1_6', 6, 10],
    ['1_4', 5, 10],
    ['1_10', 0, 5],
    ['1_11', 0, 5],
    ['1_14', 5, 10],
    ['1_13', 0, 5],
    ['1_12', 0, 5],
    ['4_1', 5, 10],
    ['4_3', 5, 10],
]

let rule_1_4 = [
    ['1_7', 6, 10],
    ['1_6', 6, 10],
    ['1_4', 5, 10],
    ['1_8', 0, 5],
    ['1_11', 0, 5],
    ['1_14', 5, 10],
    ['1_13', 0, 5],
    ['1_12', 5, 10],
    ['4_1', 5, 10],
    ['4_3', 5, 10],
    ['4_10', 5, 10],
]

let rule_2_1 = [
    ['1_7', 6, 10],
    ['1_6', 0, 5],
    ['1_8', 0, 5],
    ['1_11', 6, 10],
    ['1_10', 6, 10],
    ['1_4', 0, 5],
    ['1_13', 6, 10],
    ['4_9', 5, 10],
    ['4_2', 5, 10],
    ['4_4', 5, 10],
]

let rule_2_2 = [
    ['1_7', 6, 10],
    ['1_6', 0, 5],
    ['1_8', 6, 10],
    ['1_11', 5, 10],
    ['1_10', 5, 10],
    ['1_4', 0, 5],
    ['1_15', 4, 10],
    ['1_12', 5, 10],
    ['4_9', 5, 10],
    ['4_2', 5, 10],
    ['4_4', 5, 10],
    ['4_10', 5, 10],
]

let rule_2_3 = [
    ['1_7', 6, 10],
    ['1_6', 0, 5],
    ['1_11', 0, 5],
    ['1_10', 0, 5],
    ['1_4', 5, 10],
    ['4_3', 5, 10],
]

let rule_2_4 = [
    ['1_7', 6, 10],
    ['1_6', 0, 5],
    ['1_8', 6, 10],
    ['1_11', 0, 5],
    ['1_10', 0, 5],
    ['1_15', 5, 10],
    ['1_12', 5, 10],
    ['1_14', 5, 10],
    ['4_7', 5, 10],
    ['4_10', 5, 10],
]

let rule_3_1 = [
    ['1_7', 1, 5],
    ['1_6', 6, 10],
    ['1_11', 5, 10],
    ['1_10', 5, 10],
    ['1_9', 0, 5],
    ['1_13', 6, 10],
    ['1_8', 0, 5],
    ['4_1', 5, 10],
    ['4_9', 5, 10],
    ['4_2', 5, 10],
    ['4_4', 5, 10],
    ['4_10', 5, 10],
    ['1_1', 0, 6],
]

let rule_3_2 = [
    ['1_7', 1, 5],
    ['1_6', 6, 10],
    ['1_11', 5, 10],
    ['1_10', 5, 10],
    ['1_9', 0, 5],
    ['4_1', 5, 10],
    ['4_9', 5, 10],
    ['4_2', 5, 10],
    ['4_5', 5, 10],
    ['4_4', 5, 10],
    ['4_10', 5, 10],
]

let rule_3_3 = [
    ['1_1', 0, 6],
    ['1_7', 1, 5],
    ['1_6', 6, 10],
    ['1_10', 0, 5],
    ['1_5', 5, 10],
    ['1_11', 0, 5],
    ['1_9', 0, 5],
    ['1_13', 6, 10],
    ['4_1', 5, 10],
    ['4_5', 5, 10],
]

let rule_3_4 = [
    ['1_7', 1, 5],
    ['1_6', 6, 10],
    ['1_11', 5, 10],
    ['1_10', 5, 10],
    ['1_9', 0, 5],
    ['4_1', 5, 10],
    ['4_9', 5, 10],
    ['4_2', 5, 10],
    ['1_15', 0, 5],
    ['4_3', 0, 5],
    ['4_10', 5, 10],
]

let rule_4_1 = [
    ['1_7', 0, 5],
    ['1_6', 0, 5],
    ['1_11', 5, 10],
    ['1_10', 5, 10],
    ['1_8', 0, 5],
    ['1_13', 5, 10],
    ['4_9', 5, 10],
    ['4_2', 5, 10],
    ['4_4', 5, 10],
    ['4_7', 5, 10],
]

let rule_4_2 = [
    ['1_7', 0, 5],
    ['1_6', 0, 5],
    ['1_11', 5, 10],
    ['1_10', 5, 10],
    ['1_8', 5, 10],
    ['1_12', 5, 10],
    ['1_13', 5, 10],
    ['4_9', 5, 10],
    ['4_10', 5, 10],
    ['4_4', 5, 10],
]

let rule_4_3 = [
    ['1_14', 6, 10],
    ['1_7', 1, 5],
    ['1_8', 6, 10],
    ['1_6', 1, 5],
    ['1_14', 6, 10],
    ['1_11', 0, 5],
    ['1_10', 0, 5],
]

let rule_4_4 = [
    ['1_7', 0, 5],
    ['1_6', 0, 5],
    ['1_11', 0, 5],
    ['1_10', 0, 5],
    ['1_8', 5, 10],
    ['1_12', 5, 10],
    ['4_2', 0, 5],
    ['4_10', 5, 10],
]

let rules = [
    rule_1_1,
    rule_1_2,
    rule_1_3,
    rule_1_4,
    rule_2_1,
    rule_2_2,
    rule_2_3,
    rule_2_4,
    rule_3_1,
    rule_3_2,
    rule_3_3,
    rule_3_4,
    rule_4_1,
    rule_4_2,
    rule_4_3,
    rule_4_4
]

// function route_handler(route_index) {
//     switch (route_index) {
//         case 1:
//             project_name = $('.company-chosen').text().trim()
//             company_id = $('.company-chosen').data('company-id')
//             console.log(company_id)
//             $.ajax({
//                 headers: {"X-CSRFToken": token},
//                 url: url_get_project_participants,
//                 type: 'POST',
//
//                 data: JSON.stringify({
//                     'company': $('.company-chosen').text().trim(),
//                     'company_id': company_id
//                 }),
//                 processData: false,
//                 contentType: false,
//                 error: function (data) {
//                     toastr.error('Ошибка', data)
//                 },
//                 success: function (data) {
//                     let participants = data['participants'];
//                     console.log(participants)
//                     let html = ''
//                     for (let i = 0; i < participants.length; i++) {
//                         html += '<tr class="table-row cursor-pointer project-participant-added" id="participant_id_' + participants[i]['id'] + '">'
//                         html += '<td>' + participants[i]['name'] + '</td>'
//                         html += '<td>' + participants[i]['email'] + '</td>'
//                         html += '</tr>'
//                     }
//                     $('#wizard1-tbody-1').html(html)
//                     console.log('wizard1-tbody-1 - ' + $('#wizard1-tbody-1').html())
//                     process_table('.team-table')
//                     btn_text($('#next'), '<svg viewBox="0 0 24 24" width="24" height="24" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round" class="css-i6dzq1"><polyline points="9 18 15 12 9 6"></polyline></svg>')
//
//                     route_menu_handler(route_index, 'next')
//
//                     $('#wizard1-h-1').css('display', 'block')
//                     $('#wizard1-p-1').css('display', 'block')
//                     $('#wizard1-h-0').css('display', 'none')
//                     $('#wizard1-p-0').css('display', 'none')
//
//                 }
//             });
//
//             break;
//         case 2:
//
//             if ($('.table-row-report')[0]) {
//                 console.log(`.table-row-report')[0] -`)
//                 console.log($('.table-row-report')[0])
//                 btn_spinner($('#next'))
//
//                 let report_participants = []
//                 $('.table-row-report').each(function () {
//                     report_participants.push($(this).find(':nth-child(2)').text())
//                 })
//                 $.ajax({
//                     headers: {"X-CSRFToken": token},
//                     url: url_get_report_participants_data,
//                     type: 'POST',
//
//                     data: JSON.stringify({
//                         'report_participants': report_participants,
//                     }),
//                     processData: false,
//                     contentType: false,
//                     error: function (data) {
//                         toastr.error('Ошибка', data)
//                     },
//                     success: function (data) {
//
//                         console.log(data)
//                         let participants_data = data['participants_data']
//                         let squares_data = data['squares_data']
//                         console.log(squares_data)
//                         let html = ''
//                         for (let i = 0; i < participants_data.length; i++) {
//                             let participant_squares = participants_data[i]['participant_squares']
//                             let html = ''
//
//
//                             html += '<tr class="table-row-undistributed-participant" style="">'
//                             html += '<td class="bold-participant" style="text-align: center;vertical-align: middle;"><input class="checkbox-custom" style="width: 16px; height: 16px" type="checkbox" name="" value="0"></label></td>'
//                             html += '<td class="participant-group" style="text-align: center;vertical-align: middle;"><input class="checkbox-custom" style="width: 16px; height: 16px" type="checkbox" name="" value="0"></label></td>'
//                             html += '<td class="fio">' + participants_data[i]['fio'] + '</td>'
//                             html += '<td class="email">' + participants_data[i]['email'] + '</td>'
//                             html += '<td class="role_name">' + participants_data[i]['role_name'] + '</td>'
//                             html += '<td class="position">' + participants_data[i]['position'] + '</td>'
//
//                             html += '<td>'
//                             if (participant_squares.length > 0) {
//                                 for (let j = 0; j < participant_squares.length; j++) {
//                                     html += '<div>'
//                                     html += `${participant_squares[j]['square_code']} - ${participant_squares[j]['square_name']} (${participant_squares[j]['percentage']}%)`
//                                     html += '</div>'
//                                 }
//
//                             } else {
//                                 html += 'Отсутствует'
//                             }
//
//
//                             html += '</td>'
//                             html += '<td>'
//                             html += '<select name="category" class="form-control form-select select2 category-selected" data-bs-placeholder="Выберите категорию">'
//                             html += '<option value=""></option>'
//
//                             squares_data.forEach(function (item) {
//                                 html += `<option value="${item['square_role_name']}">${item['code']} - ${item['square_name']} - ${item['square_role_name']}</option>`
//                             })
//
//                             html += '</select>'
//                             html += '</td>'
//                             html += '</tr>'
//
//
//                             $('#tbody_undistributed_participants').append(html)
//
//                             $('#wizard1-h-2').css('display', 'block')
//                             $('#wizard1-p-2').css('display', 'block')
//                             $('#wizard1-h-1').css('display', 'none')
//                             $('#wizard1-p-1').css('display', 'none')
//                             if ($('.table-row-undistributed-participant').length > 0) {
//                                 $('#next').addClass('disabled')
//                                 $('#undistributed-participants-table').removeClass('d-none')
//                                 //
//                             } else {
//                                 $('#next').removeClass('disabled')
//                                 $('#undistributed-participants-table').addClass('d-none')
//                             }
//                             $('#next').text('Создать отчет')
//
//                         }
//
//                     }
//                 });
//
//
//                 // {#console.log(report_participants)#}
//                 console.log('fffffffff')
//                 route_menu_handler(route_index, 'next')
//             } else {
//                 toastr.error('Участники не выбраны')
//             }
//             break;
//         case 3:
//             Swal.fire({
//                 title: 'Комментарии к отчету',
//                 text: "Добавить комментарии к отчету?",
//                 icon: 'question',
//                 showCancelButton: true,
//                 confirmButtonColor: '#3085d6',
//                 cancelButtonColor: '#d33',
//                 confirmButtonText: 'Да',
//                 cancelButtonText: 'Нет'
//             }).then((result) => {
//                 if (result.value) {
//                     $('#input-modal-report-comments').modal('show')
//                 } else {
//                     save_report()
//                 }
//             })
//
//             break;
//         case 4:
//
//             break;
//         default:
//             break;
//     }
//
// }

$('#modal_comments_create_report').on('click', function () {
    $('#input-modal-report-comments').modal('hide')
    save_report()
})

function save_report() {
    btn_spinner($('#create_group_report'))
    let square_results = []
    $('.list-group-square').each(function () {
        let square_name = get_square_name_by_listgroup_id($(this).attr('id'))
        let square_code = $(this).attr('id').split('_')[1] + '_' + $(this).attr('id').split('_')[2]
        // {#console.log($(this).attr('id'))#}
        $(this).find('li').each(function () {
            square_results.push([square_name, $(this).attr('id'), $(this).text(), $(this).data('bold'), $(this).data('group-name'), $(this).data('group-color'), square_code, $(this).data('participant-number'), $(this).data('participant-id')])
        })
    })
    // console.log(square_results)

    $.ajax({
        headers: {"X-CSRFToken": token},
        url: url_save_group_report_data,
        type: 'POST',

        data: JSON.stringify({
            'square_results': square_results,
            'project': project_name,
            'company_id': company_id,
            'comments': $('#report-comments-text').val(),
            'group_report_id': group_report_id,
            'operation': 'edit'
        }),
        processData: false,
        contentType: false,
        error: function (data) {
            toastr.error('Ошибка', data)
            // console.log(data)
        },
        success: function (data) {
            // console.log('succes - ' + data['file_name'])

            let output_html = '<h2 class="mb-0" style="text-align: center">Отчет успешно создан</h2>' +
                '<br>' +
                '<hr class="solid mt-0" style="background-color: black;">' +
                '<h4 style="text-align: center">Скачать файл отчета?</h4>' +
                '<hr class="solid mt-0" style="background-color: black;">'

            Swal.fire({
                html: output_html,
                icon: 'success',
                showCancelButton: true,
                confirmButtonColor: '#3085d6',
                cancelButtonColor: '#d33',
                confirmButtonText: 'Да',
                cancelButtonText: 'Нет'
            }).then((result) => {
                if (result.value) {
                    let a = document.createElement("a");
                    a.setAttribute('target', '_blank')
                    a.href = '/panel/download_group_report/' + data['file_name'];
                    a.click();
                    setTimeout(function () {
                        // {#location.href = {% url 'panel_home' %}#}
                        window.location.reload()
                    }, 1500)
                } else {
                    window.location.reload()
                    // {#location.href = {% url 'panel_home' %}#}
                }
            })


            $('#next').removeClass('disabled').html('<svg viewBox="0 0 24 24" width="24" height="24" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round" class="css-i6dzq1"><polyline points="9 18 15 12 9 6"></polyline></svg>')


        }
    });

}


let enabled_route_number = 0
// выбор проекта
$('#menu_distribution').closest('.slide').addClass('is-expanded')
$('#menu_distribution').addClass('active')
$(".table-row").on('click', function (e) {
    $(".table-row").css('background-color', '').css('color', '').removeClass('company-chosen')
    $(this).css('background-color', '#6c5ffc').css('color', 'white').addClass('company-chosen')
    $('#next').removeClass('disabled')
})


function btn_spinner(element) {
    $(element).html('<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true" style="width: 25px;height: 25px"></span>').addClass('disabled')
}

function btn_text(element, text) {
    $(element).html(text).removeClass('disabled')
}

let table = ''

$('#main-container').on('click', '.project-participant-added', function () {
    $(this).removeClass('project-participant-added').addClass('project-participant-chosen').css('background-color', '#6c5ffc').css('color', 'white')

    // console.log($(this).find(':nth-child(1)').text())
})
$('#main-container').on('click', '.project-participant-chosen', function () {
    $(this).addClass('project-participant-added').removeClass('project-participant-chosen').css('background-color', '').css('color', '')

    // console.log($(this).find(':nth-child(1)').text())
})
$('#main-container').on('click', '.report-participant-added', function () {
    $(this).removeClass('report-participant-added').addClass('report-participant-chosen').css('background-color', '#6c5ffc').css('color', 'white')

    // console.log($(this).find(':nth-child(1)').text())
})
$('#main-container').on('click', '.report-participant-chosen', function () {
    $(this).addClass('report-participant-added').removeClass('report-participant-chosen').css('background-color', '').css('color', '')

    // console.log($(this).find(':nth-child(1)').text())
})

$('#add-all-participant').on('click', function () {
    add_participant_to_report('#wizard1-tbody-1 tr')

})

$('#add-chosen-participant').on('click', function () {

    if ($('.project-participant-chosen').length) {
        add_participant_to_report('.project-participant-chosen')
    } else {
        toastr.error('Участник не выбран')
    }

})

$('#delete-chosen-participant').on('click', function () {
    if ($('.report-participant-chosen').length) {
        delete_participant_from_report('.report-participant-chosen')
    } else {
        toastr.error('Участник не выбран')
    }

})
$('#delete-all-participant').on('click', function () {
    if ($('.report-participant-chosen').length || $('.report-participant-added').length) {
        delete_participant_from_report('#wizard1-tbody-report-1 tr')
    } else {
        toastr.error('Участники отсутствуют')
    }
})

function add_participant_to_report(element) {
    let html_report = ''
    let html_project = ''

    $(element).each(function (i, obj) {
        html_report += '<tr class="table-row-report cursor-pointer report-participant-added odd" style="">'
        html_report += $(this).html()
        html_report += '</tr>'
        $(this).remove()
    })
    html_project = $('#wizard1-tbody-1').html()
    html_report = $('#wizard1-tbody-report-1').html().trim() + html_report

    $('.team-table').DataTable().clear().destroy()
    $('#wizard1-tbody-1').append(html_project)
    $('#wizard1-tbody-report-1').empty().append(html_report.trim())
    $('#wizard1-tbody-report-1 tr').each(function () {
        if ($(this).find('td').hasClass('dataTables_empty')) {
            $(this).remove()
        }
    })
    process_table('.team-table')

}

function delete_participant_from_report(element) {
    let html_report = ''
    let html_project = ''

    $(element).each(function (i, obj) {
        html_project += '<tr class="table-row cursor-pointer project-participant-added odd">'
        html_project += $(this).html()
        html_project += '</tr>'
        $(this).remove()
    })
    html_project = $('#wizard1-tbody-1').html().trim() + html_project
    html_report = $('#wizard1-tbody-report-1').html().trim()

    $('.team-table').DataTable().clear().destroy()
    $('#wizard1-tbody-1').empty().append(html_project)

    $('#wizard1-tbody-report-1').append(html_report.trim())

    $('#wizard1-tbody-1 tr').each(function () {
        if ($(this).find('td').hasClass('dataTables_empty')) {
            $(this).remove()
        }
    })
    process_table('.team-table')

}

// распределение участников
let participants_groups = []
$('#distribute-undistributed-participants').on('click', function () {
    let category_not_selected = false
    $('.category-selected').each(function () {
        if ($(this).val() === '') {
            category_not_selected = true
        }

    })
    if (category_not_selected) {
        toastr.error('Выберите квадрат для всех нераспределенных участников')
    } else {
        let distributed_cnt = 0
        $('.table-row-undistributed-participant').each(function () {
            let fio = $(this).find('.fio').text()
            let email = $(this).find('.email').text()
            let square_name = $(this).find('.category-selected').val()
            let bold = $(this).find('td:nth-child(1) input').val()
            let group_name = $(this).find('td:nth-child(2) span').text()
            let group_color = $(this).find('td:nth-child(2)').css('background-color')
            let participant_number = $(this).find('.participant-number span').text()
            let participant_id = $(this).data('participant-id')

            let list_id = get_listgroup_id_by_name(square_name)
            $('#' + list_id).append('<li class="list-group-item" id="' + email + '" data-participant-number="' + participant_number + '" data-participant-id="' + participant_id + '" data-bold="' + bold + '" data-group-name="' + group_name + '" data-group-color="' + group_color + '">' + fio + '</li>')
            $(this).remove()
            distributed_cnt++
        })
        // let cur_distributed_cnt = parseInt($('#bage_distributed_participants').text())
        // $('#bage_distributed_participants').html(cur_distributed_cnt + distributed_cnt)
        $('.undistributed-table').DataTable().clear().destroy()
        $('#undistributed-participants-table').addClass('d-none')
        toastr.success('Участники распределены (' + distributed_cnt + ' чел.)')
        $('#create_group_report').removeClass('disabled').addClass('cursor-pointer')

    }
})

function get_listgroup_id_by_name(name) {
    let listgroup_id = ''
    switch (name) {
        case square_names_obj["1_1"]:
            listgroup_id = 'list_1_1';
            break;
        case square_names_obj["1_2"]:
            listgroup_id = 'list_1_2';
            break;
        case square_names_obj["1_3"]:
            listgroup_id = 'list_1_3';
            break;
        case square_names_obj["1_4"]:
            listgroup_id = 'list_1_4';
            break;
        case square_names_obj["2_1"]:
            listgroup_id = 'list_2_1';
            break;
        case square_names_obj["2_2"]:
            listgroup_id = 'list_2_2';
            break;
        case square_names_obj["2_3"]:
            listgroup_id = 'list_2_3';
            break;
        case square_names_obj["2_4"]:
            listgroup_id = 'list_2_4';
            break;
        case square_names_obj["3_1"]:
            listgroup_id = 'list_3_1';
            break;
        case square_names_obj["3_2"]:
            listgroup_id = 'list_3_2';
            break;
        case square_names_obj["3_3"]:
            listgroup_id = 'list_3_3';
            break;
        case square_names_obj["3_4"]:
            listgroup_id = 'list_3_4';
            break;
        case square_names_obj["4_1"]:
            listgroup_id = 'list_4_1';
            break;
        case square_names_obj["4_2"]:
            listgroup_id = 'list_4_2';
            break;
        case square_names_obj["4_3"]:
            listgroup_id = 'list_4_3';
            break;
        case square_names_obj["4_4"]:
            listgroup_id = 'list_4_4';
            break;
        default:
            break;

    }
    return listgroup_id
}

function get_square_name_by_listgroup_id(id) {
    let square_name = ''
    let square_code = ''
    switch (id) {
        case 'list_1_1':
            square_name = square_names_obj["1_1"]
            square_code = '1_1'
            break;
        case 'list_1_2':
            square_name = square_names_obj["1_2"]
            square_code = '1_2'
            break;
        case 'list_1_3':
            square_name = square_names_obj["1_3"]
            square_code = '1_3'
            break;
        case 'list_1_4':
            square_name = square_names_obj["1_4"]
            square_code = '1_4'
            break;
        case 'list_2_1':
            square_name = square_names_obj["2_1"]
            square_code = '2_1'
            break;
        case 'list_2_2':
            square_name = square_names_obj["2_2"]
            square_code = '2_2'
            break;
        case 'list_2_3':
            square_name = square_names_obj["2_3"]
            square_code = '2_3'
            break;
        case 'list_2_4':
            square_name = square_names_obj["2_4"]
            break;
        case 'list_3_1':
            square_name = square_names_obj["3_1"]
            break;
        case 'list_3_2':
            square_name = square_names_obj["3_2"]
            break;
        case 'list_3_3':
            square_name = square_names_obj["3_3"]
            break;
        case 'list_3_4':
            square_name = square_names_obj["3_4"]
            break;
        case 'list_4_1':
            square_name = square_names_obj["4_1"]
            break;
        case 'list_4_2':
            square_name = square_names_obj["4_2"]
            break;
        case 'list_4_3':
            square_name = square_names_obj["4_3"]
            break;
        case 'list_4_4':
            square_name = square_names_obj["4_4"]
            break;
        default:
            break;

    }
    return square_name
}
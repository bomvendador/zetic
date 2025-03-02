$('#wizard1-tbody-1').on('click', '.report_comments', function () {
    report_tr_id = $(this).closest('tr').attr('id')
    $('#report-comments-text').text($(this).closest('tr').find('td').eq(4).text())
    $('#input-modal-report-comments').modal('show')
})

$('#individual_reports_run_group_action').on('click', function () {
    let participants_ids_to_run_group_action = []
    let action_name = $('#individual_reports_select_group_action option:selected').val()
    if (action_name === 'no_action') {
        toastr.error('Действие для группы не выбрано')
        $('#individual_reports_select_group_action').addClass('is-invalid')
    } else {
        let selected_participants_reports_ids = []
        $('#wizard1-tbody-1 .select-participant-for-group-action:checked').each(function () {
            let tr = $(this).closest('tr')
            if (tr.find('.individual-report-icon').length > 0) {
                let report_id = tr.attr('id').split('_')[2]
                selected_participants_reports_ids.push(report_id)
            }
        })
        console.log(selected_participants_reports_ids)
        switch (action_name) {
            case "download_individual_reports":
                if (selected_participants_reports_ids.length === 0) {
                    toastr.error('Выбранные сотрудники не имеют отчетов')
                } else {
                    show_progressbar_loader()

                    let comments = $('#report-comments-text').val()
                    $.ajax({
                        headers: {"X-CSRFToken": token},
                        url: url_individual_report_group_action,
                        type: 'POST',

                        data: JSON.stringify({
                            'action_type': action_name,
                            'selected_participants_reports_ids': selected_participants_reports_ids
                        }),
                        processData: false,
                        contentType: false,
                        error: function (data) {
                            toastr.error('Ошибка', data)
                        },
                        success: function (data) {
                            console.log(data)
                            let a = document.createElement("a");
                            a.setAttribute('target', '_blank')
                            a.href = 'download_tmp_file/' + decodeURIComponent(data);
                            a.click();
                            hide_progressbar_loader()
                        }
                    });

                }


                break;

            case 'download_t_points':
                show_progressbar_loader()
                $.ajax({
                        headers: {"X-CSRFToken": token},
                        url: url_individual_report_group_action,
                        type: 'POST',

                        data: JSON.stringify({
                            'action_type': action_name,
                            'selected_participants_reports_ids': selected_participants_reports_ids
                        }),
                        processData: false,
                        contentType: false,
                        error: function (data) {
                            toastr.error('Ошибка', data)
                        },
                        success: function (response) {
                            hide_progressbar_loader()
                            let reports_data = response['reports_data']
                            let categories_names = response['categories_names']
                            let sheet_header = ['Компания', 'Участник', 'Email', 'Пол', 'Должность', 'Индустрия', 'Роль/Функция', 'Год рождения', 'Окончание заполнения']
                            let sheet_data = []
                            categories_names.forEach(function (name) {
                                sheet_header.push(name)
                            })
                            sheet_data.push(sheet_header)
                            reports_data.forEach(function (report_data) {
                                let participant_row_data = []
                                let categories_data = report_data['categories_data']
                                let company = report_data['company']
                                let participant = report_data['participant']
                                let email = report_data['email']
                                let gender = report_data['gender']
                                let position = report_data['position']
                                let industry = report_data['industry']
                                let role = report_data['role']
                                let birth_year = report_data['birth_year']
                                let completed_at = report_data['completed_at']
                                participant_row_data.push(company, participant, email, gender, position, industry, role, birth_year, completed_at)
                                categories_data.forEach(function (category) {
                                    participant_row_data.push(category['points'])
                                })
                                sheet_data.push(participant_row_data)

                            })
                            let workbook = XLSX.utils.book_new(), worksheet = XLSX.utils.aoa_to_sheet(sheet_data);
                            workbook.SheetNames.push("First");
                            workbook.Sheets["First"] = worksheet;
                            let currentdate = new Date();
                            let datetime_string = currentdate.getDate() + '_'
                                + (currentdate.getMonth() + 1).toString() + '_'
                                + currentdate.getFullYear() + " @ "
                                + currentdate.getHours() + ":"
                                + currentdate.getMinutes() + ":"
                                + currentdate.getSeconds();
                            XLSX.writeFile(workbook, '[Т-Баллы] ' + datetime_string + ".xlsx");
                        }
                    }
                );
                break;
            default:
                break;
        }
    }
})


$('#modal_save_comments_btn').on('click', function () {
    btn_spinner('#modal_save_comments_btn')
    let comments = $('#report-comments-text').val()
    $.ajax({
        headers: {"X-CSRFToken": token},
        url: url_save_individual_report_comments,
        type: 'POST',

        data: JSON.stringify({
            'report_tr_id': report_tr_id.split('_')[2],
            'comments': comments
        }),
        processData: false,
        contentType: false,
        error: function (data) {
            toastr.error('Ошибка', data)
        },
        success: function (data) {
            console.log(data)
            $('#' + report_tr_id).find('td').eq(4).text(comments)
            btn_text($('#modal_save_comments_btn'), 'Сохранить')
            $('#input-modal-report-comments').modal('hide')
            toastr.success('Комментарии сохранены')
        }
    });

})

let report_id

$('#project_participants_table').on('click', '.regenerate_report', function () {
    let tr_report_id = $(this).closest('tr').attr('id')
    report_id = tr_report_id.split('_')[2]

    $('#modal_report_options #modal_change_report_options').modal('show')


})

$('#modal_report_options').on('click', '#change_report_options_save', function () {
    let options_data = []

    $('#modal_report_options .option-for-individual-report').each(function () {
        options_data.push({
            'id': $(this).data('option-id'),
            'value': $(this).prop('checked')
        })
    })
    let btn_text_value = $('#change_report_options_save').html()
    btn_spinner($('#change_report_options_save'))
    $.ajax({
        headers: {"X-CSRFToken": token},
        url: url_pdf_regenerate_report,
        type: 'POST',

        data: JSON.stringify({
            'report_id': report_id,
            'options_data': options_data
        }),
        processData: false,
        contentType: false,
        error: function (data) {
            toastr.error('Ошибка', data)
        },
        success: function (data) {
            btn_text($('#change_report_options_save'), btn_text_value)
            console.log(data)
            let company_name = data

            let output_html = '<hr class="solid mt-0" style="background-color: black;">' +
                '<h3 style="text-align: center">Пересоздание отчета</h3>' +
                '<hr class="solid mt-0" style="background-color: black;">' +
                '<div style="text-align: center">Отчет успешно пересоздан</div>'

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

$('#project_participants_table').on('click', '.select-participant-for-group-action', function () {

    let checked_checkboxes_cnt = $('#project_participants_table .select-participant-for-group-action:checked').length
    if ($(this).prop('checked')) {
        if (checked_checkboxes_cnt === 1) {
            $('#individual_reports_select_group_action').removeAttr('disabled')
            $('#individual_reports_run_group_action').removeAttr('disabled')
        }
    } else {
        if (checked_checkboxes_cnt === 0) {
            $('#individual_reports_select_group_action').attr('disabled', true)
            $('#individual_reports_run_group_action').attr('disabled', true)
        }

    }
})
$('#select_all_participants_for_group_action').on('click', function () {
    if ($(this).prop('checked')) {
        $('#project_participants_table .select-participant-for-group-action').prop('checked', true)
        $('#individual_reports_select_group_action').removeAttr('disabled')
        $('#individual_reports_run_group_action').removeAttr('disabled')
    } else {
        $('#project_participants_table .select-participant-for-group-action').prop('checked', false)
        $('#individual_reports_select_group_action').attr('disabled', true)
        $('#individual_reports_run_group_action').attr('disabled', true)

    }
})


function route_menu_handler(route_index, btn_type) {
    let new_menu_number = 0
    if (btn_type === 'next') {
        new_menu_number = route_index + 1
    } else {
        new_menu_number = route_index - 1
    }
    switch (new_menu_number) {
        case 1:
            $('#mass_actions_block').addClass('d-none');
            break;
        case 2:
            $('#mass_actions_block').removeClass('d-none');
            break;

        default:
            break;
    }
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
        // $('#next').addClass('disabled')
        // $('#next').removeClass('cursor-pointer')
    } else {
        $('#next').removeClass('disabled')

    }

}

function route_handler(route_index) {
    btn_spinner($('#next'))
    switch (route_index) {
        case 1:
            let company_id = $('.project-chosen').data('company-id')
            $.ajax({
                headers: {"X-CSRFToken": token},
                url: url_get_individual_reports_list,
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
                    console.log(data)
                    let data_json = data['data'];
                    let modal_report_options_html = data['modal_report_option'];

                    $('#modal_report_options').html(modal_report_options_html)
                    let html = ''
                    data_json.forEach(function (item) {
                        html += `<tr class="report-row" id="report_id_${item['id']}" data-participant-id="${item['participant_id']}">`
                        html += '<td><input class="select-participant-for-group-action" type="checkbox" class="" style="transform: scale(1.1)">'
                        if (item['file_name'] !== '') {
                            html += '<i class="fe fe-file-text individual-report-icon" style="color: blue" title="Отчет создан"></i>'
                        }
                        html += '</td>'
                        html += '<td>' + item['name'] + '</td>'
                        html += '<td>' + item['email'] + '</td>'
                        html += '<td>' + item['study_name'] + '</td>'
                        html += '<td><span style="display: none">' + item['timestamp'] + '</span> ' + item['date'] + '</td>'
                        html += '<td>' + item['company'] + '</td>'
                        if (item['type'] === 'consultant_form') {
                            html += '<td>Выводы экперта</td>'
                        } else {
                            if (item['primary'] === true) {
                                html += '<td>Первичный</td>'

                            } else {
                                html += '<td>Пересозданный</td>'
                            }

                        }
                        if (cur_userprofile_role_name !== 'Админ заказчика') {
                            html += '<td>' + item['comments'] + '</td>'//комментарии
                        }

                        html += '<td>'
                        html += '<div style="text-align: center;">'
                        html += '<i class="fe fe-more-vertical cursor-pointer" data-bs-toggle="dropdown" aria-expanded="false" style="font-size: 20px"></i>'
                        html += '<ul class="dropdown-menu">'
                        if (item['file_name'] !== '') {
                            html += '<li><a class="dropdown-item" href="download_single_report/' + item['file_name'] + '">Скачать</a></li>'

                        }
                        if (cur_userprofile_role_name !== 'Партнер') {
                            html += '<li class="regenerate_report"><a class="dropdown-item cursor-pointer">Пересоздать</a></li>'
                        }
                        if (cur_userprofile_role_name !== 'Админ заказчика') {
                            html += '<li><a class="dropdown-item report_comments cursor-pointer">Комментарий</a></li>'
                        }

                        html += '</ul>'
                        html += '</div>'

                        html += '</td>'

                        html += '</tr>'

                    })

                    $('#wizard1-tbody-1').html(html)
                    process_table('#project_participants_table')
                    btn_text($('#next'), '<svg viewBox="0 0 24 24" width="24" height="24" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round" class="css-i6dzq1"><polyline points="9 18 15 12 9 6"></polyline></svg>')

                    route_menu_handler(route_index, 'next')

                    $('#wizard1-h-1').css('display', 'block')
                    $('#wizard1-p-1').css('display', 'block')
                    $('#wizard1-h-0').css('display', 'none')
                    $('#wizard1-p-0').css('display', 'none')
                    $('#next').addClass('disabled')

                }
            });

            break;
        default:
            break;
    }

}

let enabled_route_number = 0
// выбор проекта
$('#menu_individual_reports_list').closest('.slide').addClass('is-expanded')
$('#menu_individual_reports_list').addClass('active')

$(".table-row").on('click', function (e) {
    $(".table-row").css('background-color', '').css('color', '').removeClass('project-chosen')
    $(this).css('background-color', '#6c5ffc').css('color', 'white').addClass('project-chosen')
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
            $('.undistributed-table').DataTable().clear().destroy()
            $('#wizard1-h-1').css('display', 'block')
            $('#wizard1-p-1').css('display', 'block')
            $('#wizard1-h-2').css('display', 'none')
            $('#wizard1-p-2').css('display', 'none')
            $('.list-group-item').each(function () {
                $(this).remove()
            })
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
        "paging": false,
        "language": {
            "url": "//cdn.datatables.net/plug-ins/9dcbecd42ad/i18n/Russian.json"
        },
        "initComplete": function () {

        },
    })
}

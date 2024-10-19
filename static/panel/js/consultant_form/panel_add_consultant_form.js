
function route_menu_handler(route_index, btn_type) {
    let new_menu_number = 0
    if (btn_type === 'next') {
        new_menu_number = route_index + 1
    } else {
        new_menu_number = route_index - 1
    }
    console.log('new_menu_number - ' + new_menu_number)
    // {#if (new_menu_number <= 4){#}
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

    }

}


function route_handler(route_index) {
    console.log('project - ' + $('.project-chosen').text().trim())
    // {#console.log(route_index)#}
    console.log('route_index - ' + route_index)
    btn_spinner($('#next'))
    switch (route_index) {
        case 1:
            let company_id = $('.company-chosen').data('company-id')
            console.log(company_id)
            $.ajax({
                headers: {"X-CSRFToken": token},
                url: url_get_consultant_company_studies,
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

                    let studies = data['studies'];
                    let html = ''
                    studies.forEach(function (item) {
                        html += '<tr class="table-row company-study cursor-pointer" data-study-id="' + item["id"] + '">'
                        html += '<td class="">' + item['id'] + '. ' + item['name'] + '</td>'
                        html += '</tr>'
                    })

                    $('#wizard1-tbody-1').html(html)

                    process_table('#company_studies_table')
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
        case 2:
            let study_id = $('.study-chosen').data('study-id')
            console.log(study_id)
            $.ajax({
                headers: {"X-CSRFToken": token},
                url: url_get_study_participants,
                type: 'POST',

                data: JSON.stringify({
                    'study_id': study_id,
                }),
                processData: false,
                contentType: false,
                error: function (data) {
                    toastr.error('Ошибка', data)
                },
                success: function (data) {
                    console.log(data)

                    let participants = data['participants'];
                    let html = ''
                    participants.forEach(function (item) {
                        html += '<tr class="table-row participant cursor-pointer" data-participant-id="' + item["id"] + '">'
                        html += '<td class="">' + item['name'] + '</td>'
                        html += '<td class="">' + item['email'] + '</td>'
                        html += '</tr>'
                    })
                    //
                    $('#wizard1-tbody-2').html(html)

                    process_table('#participants_table')
                    btn_text($('#next'), 'Создать анкету')
                    //
                    route_menu_handler(route_index, 'next')

                    $('#wizard1-h-2').css('display', 'block')
                    $('#wizard1-p-2').css('display', 'block')
                    $('#wizard1-h-1').css('display', 'none')
                    $('#wizard1-p-1').css('display', 'none')
                    $('#next').addClass('disabled')

                }
            });

            break;
        case 3:
            let participant_id = $('.participant-chosen').data('participant-id')

            console.log(participant_id)
            window.location.href = 'add_consultant_form_template/' + participant_id
            break;
        default:
            break;
    }

}

let enabled_route_number = 0
// выбор проекта
$('#menu_individual_reports_list').closest('.slide').addClass('is-expanded')
$('#menu_individual_reports_list').addClass('active')

$("#content_div").on('click', '.company-study', function (e) {
    $(".company-study").css('background-color', '').css('color', '').removeClass('study-chosen')
    $(this).css('background-color', '#6c5ffc').css('color', 'white').addClass('study-chosen')
    $('#next').removeClass('disabled')
})

$("#content_div").on('click', '.participant', function (e) {
    $(".company-study").css('background-color', '').css('color', '').removeClass('participant-chosen')
    $(this).css('background-color', '#6c5ffc').css('color', 'white').addClass('participant-chosen')
    $('#next').removeClass('disabled')
})

$(".company").on('click', function (e) {
    $(".table-row").css('background-color', '').css('color', '').removeClass('company-chosen')
    $(this).css('background-color', '#6c5ffc').css('color', 'white').addClass('company-chosen')
    $('#next').removeClass('disabled')
})

$('#next').on('click', function () {
    if ($(this).hasClass('disabled')) {
        if (enabled_route_number === 1) {
            toastr.error('Выберите компанию')
        }
    } else {
        // {#$(this).find('a').html('<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true" style="width: 25px;height: 25px;"></span>')#}
        $('.route-item').each(function (i, obj) {
            if (!$(this).hasClass('disabled')) {
                enabled_route_number = parseInt($(this).find('.number').html())

            }
            // {#route_menu_handler($(this).find('.number').html())#}

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
        // {#route_menu_handler($(this).find('.number').html())#}

    })
    switch (enabled_route_number) {
        case 2:
            // {#$('#wizard1-tbody-1').html('')#}
            // {#process_table('.team-table')#}
            $('.team-table').DataTable().clear().destroy()
            $('#wizard1-h-1').css('display', 'none')
            $('#wizard1-p-1').css('display', 'none')
            $('#wizard1-h-0').css('display', 'block')
            $('#wizard1-p-0').css('display', 'block')
            $(this).addClass('disabled')
            break;
        case 3:
            // {#$('#wizard1-tbody-1').html('')#}
            // {#process_table('.team-table')#}
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

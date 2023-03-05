expand_menu_item('#menu_study_list')

let table = process_table('.team-table')

function process_circle_progress(){
    $('svg.radial-progress').each(function( index, value ) {
        // If svg.radial-progress is approximately 25% vertically into the window when scrolling from the top or the bottom
            // Get percentage of progress
            let percent = $(value).data('percentage');
            // Get radius of the svg's circle.complete
            let radius = $(this).find($('circle.complete')).attr('r');
            // Get circumference (2πr)
            let circumference = 2 * Math.PI * radius;
            // Get stroke-dashoffset value based on the percentage of the circumference
            let strokeDashOffset = circumference - ((percent * circumference) / 100);
            // Transition progress for 1.25 seconds
            $(this).find($('circle.complete')).animate({'stroke-dashoffset': strokeDashOffset}, 1250);
            // if(percent === 100){
            //
            // }

        });
}

process_circle_progress()

$('#tbody_participants_selected').on('click', '.add-question-groups', function () {
    show_progressbar_loader()
    let html = ''
    let participant_tr_id = $(this).closest('tr').attr('id')
    let participant_tr_p = $('#' + participant_tr_id).find('.participant_selected_questions_groups_td p')
    $('#tbody_question_groups_selected tr').each(function () {
        let questions_group_code_modal = $(this).attr('id').split('_')[2]
        let question_exists = false

        participant_tr_p.each(function () {
            let questions_group_code_participant_selected = $(this).attr('id').split('_')[5]
            if(questions_group_code_modal === questions_group_code_participant_selected){
                question_exists = true
            }
        })
        if(question_exists){
            html += '<tr class="question_group_item question_group_selected cursor-pointer" id="modal' + $(this).attr("id") + '">'
        }else {
            html += '<tr class="question_group_item cursor-pointer" id="modal' + $(this).attr("id") + '">'
        }

        html += '<td>' + $(this).children('td').eq(0).text() + '</td>'
        html += '<td></td>'
        html += '</tr>'

    })
    let el = $('#tbody_modal_questions_groups')
    el.html(html)
    el.attr('data-participant-tr-id', participant_tr_id)

    hide_progressbar_loader()
    $('#modal_question_groups').modal('show')
})

$('#tbody_modal_questions_groups').on('click', '.question_group_item', function(){
    if($(this).hasClass('question_group_selected')){
        $(this).removeClass('question_group_selected')
    }else {
        $(this).addClass('question_group_selected')
    }
})

$('#select_all_question_groups').on('click', function () {
    if ($(this).attr('checked') === 'checked'){
        $(this).attr('checked', false)
        $('#tbody_modal_questions_groups').find('.question_group_item').each(function () {
            $(this).removeClass('question_group_selected')
        })
        // active = 0
    }else {
        $(this).attr('checked', 'checked')
        $('#tbody_modal_questions_groups').find('.question_group_item').each(function () {
            $(this).addClass('question_group_selected')
        })

        // active = 1
    }
})

$('#save_question_groups').on('click', function () {
    let questions_groups_selected = []

    $('#tbody_modal_questions_groups').find('.question_group_selected').each(function () {
        let code = $(this).attr('id').split('_')[2]
        questions_groups_selected.push({
            'name': $(this).find('td').text(),
            'code': code
        })
    })
    if(questions_groups_selected.length === 0){
        toastr.error('Выберите группу(ы) вопросов')
    }else {
        let participant_tr_id = $('#tbody_modal_questions_groups').attr('data-participant-tr-id')
        let participant_id = participant_tr_id.split('_')[2]
        let data = {
            'questions_groups_selected': questions_groups_selected,
            'participant_id': participant_id,
        }
        btn_spinner($('#save_question_groups'))
        $.ajax({
            headers: { "X-CSRFToken": token },
            url: url_save_participant_questions_groups,
            type: 'POST',

            data: JSON.stringify({
                            'data': data,
                            'study_id': study_id
                        }),
            processData: false,
            contentType: false,
            error: function(data){
                toastr.error('Ошибка', data)
            },
            success:function (data) {
                let role_name = $('#cur_role_name').text()
                console.log(data)
                let data_json = data['response']
                if(data_json === 'logout'){
                    window.location.href = url_login_home
                }else {
                    if (data_json === 'company_deactivated' && role_name === 'Админ заказчика') {
                        $('#modal_question_groups').modal('hide')
                        btn_text($('#save_question_groups'), 'Сохранить')

                        let output_html = '<hr class="solid mt-0" style="background-color: black;">' +
                            '<div>Компания деактивирована' + '</div>' +
                            '<div>Если Вы не знаете причин - обратитесь к менеджеру' + '</div>' +
                            '<br>' +
                            '<hr class="solid mt-0" style="background-color: black;">'
                        Swal.fire({
                            html: output_html,
                            icon: 'warning',
                            confirmButtonColor: '#3085d6',
                            cancelButtonColor: '#d33',
                            confirmButtonText: 'ОК'
                        })
                    } else {
                        if (data['warning']) {
                            toastr.warning(data['warning'])
                        }


                        let html = ''
                        for (let i = 0; i < questions_groups_selected.length; i++) {
                            let questions_group_selected = questions_groups_selected[i]
                            html += '<p class="mb-0 participant-selected-question-group" id="participant_selected_question_group_id_' + questions_group_selected['code'] + '">' + questions_group_selected['name'] + '</p>'
                        }
                        let el = $('#' + participant_tr_id).find('.participant_selected_questions_groups_td')
                        el.html('')
                        el.html(html)
                        $('#modal_question_groups').modal('hide')
                        btn_text($('#save_question_groups'), 'Сохранить')
                        toastr.success('Группы вопросов сохранены')


                    }

                }



            }
        });



    }


})


$('#add_participant').on('click', function () {
    show_progressbar_loader()
    $.ajax({
        headers: { "X-CSRFToken": token },
        url: url_get_employees_for_study,
        type: 'POST',

        data: JSON.stringify({
                            'study_id': study_id
                        }),
        processData: false,
        contentType: false,
        error: function(data){
            toastr.error('Ошибка', data)
        },
        success:function (data) {
            let role_name = $('#cur_role_name').text()
            console.log(data)
            hide_progressbar_loader()
            let data_json = data['response']
            if(data_json === 'logout'){
                window.location.href = url_login_home
            }else {
                if(data_json === 'None'){

                    let output_html = '<hr class="solid mt-0" style="background-color: black;">' +
                                    '<div>Cотрудники для распределения отсутстуют' + '</div>' +
                                    '<br>' +
                                    '<hr class="solid mt-0" style="background-color: black;">'
                    Swal.fire({
                      html: output_html,
                      icon: 'warning',
                      confirmButtonColor: '#3085d6',
                      cancelButtonColor: '#d33',
                      confirmButtonText: 'ОК'
                    })
                }else{
                    if (data_json === 'company_deactivated' && role_name === 'Админ заказчика'){
                        let output_html = '<hr class="solid mt-0" style="background-color: black;">' +
                                        '<div>Компания деактивирована' + '</div>' +
                                        '<div>Если Вы не знаете причин - обратитесь к менеджеру' + '</div>' +
                                        '<br>' +
                                        '<hr class="solid mt-0" style="background-color: black;">'
                        Swal.fire({
                          html: output_html,
                          icon: 'warning',
                          confirmButtonColor: '#3085d6',
                          cancelButtonColor: '#d33',
                          confirmButtonText: 'ОК'
                        })
                    }else {
                        if(data['warning']){
                            toastr.warning(data['warning'])
                        }
                        let html = ''
                        for(let i=0; i < data_json.length; i++) {
                            console.log('id - ' + data_json[i]['participant_id'] + 'len - ' + $('#tbody_participants_selected').find('#participant_id_' + data_json[i]['participant_id']).length)
                            if($('#tbody_participants_selected').find('#participant_id_' + data_json[i]['participant_id']).length > 0){
                                html += '<tr class="participant_item participant_item_selected cursor-pointer" id="employee_id_' + data_json[i]['employee_id'] + '">'
                            }else {
                                html += '<tr class="participant_item  cursor-pointer" id="employee_id_' + data_json[i]['employee_id'] + '">'
                            }
                            html += '<td class=" employee-name">' + data_json[i]['name'] + '</td>'
                            html += '<td class="text-end employee-email">' + data_json[i]['email'] + '</td>'
                            html += '</tr>'
                        }
                        $('#tbody_modal_participants').html(html)
                        $('#modal_participants').modal('show')
                    }

                }
            }
        }
    });


})

$('#select_all_participants').on('click', function () {
    if ($(this).attr('checked') === 'checked'){
        $(this).attr('checked', false)
        $('#tbody_modal_participants').find('.participant_item').each(function () {
            $(this).removeClass('participant_item_selected')
        })
        // active = 0
    }else {
        $(this).attr('checked', 'checked')
        $('#tbody_modal_participants').find('.participant_item').each(function () {
            $(this).addClass('participant_item_selected')
        })

        // active = 1
    }
})

$('#tbody_modal_participants').on('click', '.participant_item', function(){
    if($(this).hasClass('participant_item_selected')){
        $(this).removeClass('participant_item_selected')
    }else {
        $(this).addClass('participant_item_selected')
    }
})

$('body').on('click', 'a[data-action=create_questionnaire]', function() {
  const participant_id = $(this).data('participant-id');
  const toast = toastr.info('Создаём анкету', `${study_id} -> ${participant_id}`, {timeOut: 0})

  $.ajax({
    headers: { "X-CSRFToken": token },
    url: url_create_questionnaire,
    type: 'POST',

    data: JSON.stringify({
      'study_id': study_id,
      'participant_id': participant_id
    }),
    processData: false,
    contentType: false,
    error: function(data){
      toastr.error('Ошибка', data)
    },
    success: function(data){
      toast.success("Успех")
      window.location.reload()
    },
    complete: function() {
      toast.remove()
    },
  })

})

$('#save_participants').on('click', function () {
    const employees_ids = []
    const employees_selected = {}

    $('#tbody_modal_participants').find('.participant_item_selected').each(function () {
        let id = $(this).attr('id').split('_')[2]
        employees_ids.push(id)
        employees_selected[id] = {
            'name': $(this).find('.employee-name').text(),
            'id': id,
            'email': $(this).find('.employee-email').text()
        }
    })
    if(employees_ids.length === 0){
        toastr.error('Выберите участников')
    } else {
        let data = {
            'employees_ids': employees_ids,
            'study_id': study_id,
            'send_email': $('#select_send_email').is(':checked'),
        }
        btn_spinner($('#save_participants'))
        $.ajax({
            headers: { "X-CSRFToken": token },
            url: url_save_study_participants,
            type: 'POST',

            data: JSON.stringify({
                            'data': data
                        }),
            processData: false,
            contentType: false,
            error: function(data){
                toastr.error('Ошибка', data)
            },
            success:function (data) {
                $('.team-table').DataTable().clear().destroy()
                let data_json = data['response']
                let html = ''
                console.log(data_json)
                $.each(data_json, function (key, val) {
                    let employee_invitation = val['invitation']
                    let invitation_code = val['invitation_code']
                    let employee_email = val['email']
                    let employee_name = val['name']
                    let id = val['id']

                    let employee_invitation_sent_datetime = val['invitation_sent_datetime']
                    let completed_at_datetime = val['completed_at_datetime']
                    let reminder = val['reminder']
                    let questions_groups_arr = val['questions_groups_arr']
                    let current_percentage = val['current_percentage']
                    let total_questions_qnt = val['total_questions_qnt']
                    let answered_questions_qnt = val['answered_questions_qnt']
                    let filename = val['filename']
                    html += '<tr class="" id="participant_id_' + id + '">'
                    html += '<td>'
                    if(answered_questions_qnt > 0){

                        if(completed_at_datetime){
                            html += '<i class="fa fa-circle font-color-success" aria-hidden="true" title="Опросник заполнен"><span style="color: transparent">3</span></i>'
                        }else {
                            html += '<i class="fa fa-circle font-color-warning" aria-hidden="true" title="Приглашение отправлено"><span style="color: transparent">2</span></i>'
                        }
                        html += '<span title="' + current_percentage + '%">'
                        html += '<svg class="radial-progress" data-percentage="' + current_percentage + '" viewBox="0 0 80 80">'
                        html += '<circle class="incomplete" cx="40" cy="40" r="35"></circle>'
                        html += '<circle class="complete" cx="40" cy="40" r="35" style="stroke-dashoffset: 39.58406743523136;"></circle>'
                        html += '</svg>'
                        html += '</span>'

                    }else {
                        html += '<i class="fa fa-circle font-color-danger" aria-hidden="true" title="Приглашение не отправлено"><span style="color: transparent">1</span></i>'
                    }
                    html += '</td>'
                    html += '<td>' + answered_questions_qnt + '/' + total_questions_qnt + '</td>'
                    html += '<td>' + employee_name + '</td>'
                    html += '<td>' + employee_email + '</td>'

                    html += '<td class="participant_selected_questions_groups_td">'
                    for(let i = 0; i < questions_groups_arr.length; i++){
                        html += '<p class="mb-0 participant-selected-question-group" id="participant_selected_question_group_id_' + questions_groups_arr[i]['code'] +
                            '">' + questions_groups_arr[i]['name'] + '</p>'
                    }
                    html += '</td>'

                    html += '<td>' + employee_invitation_sent_datetime + '</td>'
                    if(reminder !== ''){
                        html += '<td>'
                        for(let i=0; i < reminder.length; i++){
                            html += reminder[i] + '<br>'
                        }
                        html += '</td>'
                    }else {
                        html += '<td></td>'
                    }

                    html += '<td>' +
                        '<div style="text-align: center;" >' +
                            '<i class="fe fe-more-vertical cursor-pointer" data-bs-toggle="dropdown" aria-expanded="false" style="font-size: 20px"></i>' +
                            '<ul class="dropdown-menu">'
                    if(employee_invitation){
                        if(completed_at_datetime){
                            html += '<li><a class="dropdown-item" href="/panel/download_single_report/' + filename + '">Скачать</a></li>'
                        }else {
                            html += '<li><a class="dropdown-item send-email-invitation cursor-pointer">Повторно отправить приглашение</a></li>'
                        }
                    }else {
                        if (!invitation_code) {
                            html += '<li><a class="dropdown-item send-email-invitation cursor-pointer">Создать анкету</a></li>'
                        }
                        html += '<li><a class="dropdown-item send-email-invitation cursor-pointer">Отправить приглашение</a></li>'
                        html += '<li> <a class = "dropdown-item add-question-groups cursor-pointer">Добавить группы вопросов</a></li>'
                    }
                    html += '</ul>' +
                        '</div>' +
                        '</td>'
                    html += '</tr>'

                })
                $('#tbody_participants_selected').html(html)
                process_circle_progress()
                $('#modal_participants').modal('hide')
                btn_text($('#save_participants'), 'Сохранить')
                toastr.success('Участники обновлены')
                process_table_clear('.team-table')
                // $('.team-table').DataTable().raw(html).add()

            }
        });



    }


})

$('#modal_send_invitation_btn').on('click', function () {
    btn_spinner('#modal_send_invitation_btn')
    let participant_tr_id = $('#modal_participant_name').attr('data-tr-id')
    let participant_tr = $('#' + participant_tr_id)
    let participant_id = participant_tr_id.split('_')[2]
    let send_admin_notification_after_filling_up = 0
    if ($('#send_admin_notification_after_filling_up').attr('checked') === 'checked') {
        send_admin_notification_after_filling_up = 1
    }
    $.ajax({
        headers: { "X-CSRFToken": token },
        url: url_send_invitation_email,
        type: 'POST',

        data: JSON.stringify({
                            'study_id': study_id,
                            'participant_id': participant_id,
                            'type': 'initial',
                            'send_admin_notification_after_filling_up': send_admin_notification_after_filling_up
                        }),
        processData: false,
        contentType: false,
        error: function(data){
            toastr.error('Ошибка', data)
        },
        success:function (data) {
            let json_data = data['response']
            if('error' in json_data){
                toastr.error(json_data['error'])
            }else {
                if('company_error' in json_data){
                    if(json_data['company_error'] === 'company_deactivated'){
                        let output_html = '<hr class="solid mt-0" style="background-color: black;">' +
                                        '<div>Компания деактивирована' + '</div>' +
                                        '<div>Если Вы не знаете причин - обратитесь к менеджеру' + '</div>' +
                                        '<br>' +
                                        '<hr class="solid mt-0" style="background-color: black;">'
                        Swal.fire({
                          html: output_html,
                          icon: 'warning',
                          confirmButtonColor: '#3085d6',
                          cancelButtonColor: '#d33',
                          confirmButtonText: 'ОК'
                        })
                    }
                }else {
                    let datetime_invitation_sent = json_data['datetime_invitation_sent'];
                    let el = $('#participant_id_' + participant_id)
                    el.find('.font-color-danger').removeClass('font-color-danger').addClass('font-color-warning').prop('title', 'Приглашение отправлено')
                    el.find('.send-email-invitation').text('Повторно отправить приглашение')
                    el.find('td:nth-child(6)').text(datetime_invitation_sent)
                    el.find('td:nth-child(2)').text('0/' + json_data['questions_count'])
                    toastr.success('Приглашение участнику отправлено')
                }
            }

            btn_text('#modal_send_invitation_btn', 'Отправить')
            $('#modal_before_send_invitation').modal('hide')


        }
    });

})


$('#tbody_participants_selected').on('click', '.send-email-invitation', function () {
    let role_name = $('#cur_role_name').text()
    if ($('#company_active').attr('checked') !== 'checked' && role_name !== 'Админ заказчика') {
        toastr.warning('Обратите внимание - компания деактивирована!')
    }

    let question_groups_qnt = $(this).closest('tr').find('.participant_selected_questions_groups_td p').length
    if(question_groups_qnt === 0){
        toastr.error('Выберите группы вопросов для участника')
    }else {
        let participant_name = $(this).closest('tr').find('td').eq(2).text()
        let participant_email = $(this).closest('tr').find('td').eq(3).text()
        $('#modal_participant_name').html('<b>' + participant_name + '</b>').attr('data-tr-id', $(this).closest('tr').attr('id'))
        $('#modal_participant_email').html('<b>' + participant_email + '</b>')
        $('#modal_before_send_invitation').modal('show')
    }
})

$('#send_admin_notification_after_filling_up').on('click', function () {
    if ($(this).attr('checked') === 'checked'){
        $(this).attr('checked', false)
        // active = 0
    }else {
        $(this).attr('checked', 'checked')
        // active = 1
    }
})



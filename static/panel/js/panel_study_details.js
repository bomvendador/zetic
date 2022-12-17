expand_menu_item('#menu_study_add')

$('#add_question_group').on('click', function () {
    show_progressbar_loader()
    $.ajax({
        headers: { "X-CSRFToken": token },
        url: url_get_question_groups,
        type: 'POST',

        data: '',
        processData: false,
        contentType: false,
        error: function(data){
            toastr.error('Ошибка', data)
        },
        success:function (data) {
            hide_progressbar_loader()
            let data_json = data['response']
            let html = ''
            for(let i=0; i < data_json.length; i++) {
                html += '<tr class="question_group_item" id=section_id_' + data_json[i]['id'] + '>'
                html += '<td>' + data_json[i]['name'] + '</td>'
                html += '<td></td>'
                html += '</tr>'
            }
            $('#tbody_modal_questions_groups').html(html)
        }
    });


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
let questions_groups_ids = []
let questions_groups_selected = {}

    $('#tbody_modal_questions_groups').find('.question_group_selected').each(function () {
        let id = $(this).attr('id').split('_')[2]
        questions_groups_ids.push(id)
        questions_groups_selected[id] = $(this).find('td').text()
    })
    if(questions_groups_ids.length === 0){
        toastr.error('Выберите группу(ы) вопросов')
    }else {
        let data = {
            'questions_groups_ids': questions_groups_ids,
            'study_id': study_id
        }
        btn_spinner($('#save_question_groups'))
        $.ajax({
            headers: { "X-CSRFToken": token },
            url: url_save_study_questions_groups,
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
                let html = ''
                $.each(questions_groups_selected, function (key, val) {
                    html += '<tr class="question_group_item_selected" id="selected_section_id_' + key + '">'
                    html += '<td>' + val + '</td>'
                    html += '<td></td>'
                    html += '</tr>'

                })
                $('#tbody_question_groups_selected').html(html)
                $('#modal_question_groups').modal('hide')
                btn_text($('#save_question_groups'), 'Сохранить')
                toastr.success('Группы вопросов сохранены')

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
            hide_progressbar_loader()
            let data_json = data['response']
            if(data_json === 'None'){

                let output_html = '<hr class="solid mt-0" style="background-color: black;">' +
                                '<div>У компании сотрудники отсутстуют' + '</div>' +
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
                let html = ''
                for(let i=0; i < data_json.length; i++) {
                    html += '<tr class="participant_item" id="employee_id_' + data_json[i]['id'] + '">'
                    html += '<td class=" employee-name">' + data_json[i]['name'] + '</td>'
                    html += '<td class="text-end employee-email">' + data_json[i]['email'] + '</td>'
                    html += '</tr>'
                }
                $('#tbody_modal_participants').html(html)
                $('#modal_participants').modal('show')

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

$('#save_participants').on('click', function () {
let employees_ids = []
let employees_selected = {}

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
    }else {
        let data = {
            'employees_ids': employees_ids,
            'study_id': study_id
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
                let data_json = data['response']
                let html = 'data_json'
                $.each(data_json, function (key, val) {
                    let employee_invitation = val['invitation']
                    let employee_email = val['email']
                    let employee_name = val['name']
                    let id = val['id']

                    let employee_invitation_sent_datetime = val['invitation_sent_datetime']
                    html += '<tr class="" id="participant_id_' + id + '">'
                    if(employee_invitation){
                        html += '<td><span class="dot-label bg-warning" title="Приглашение отправлено"></span></td>'
                    }else {
                        html += '<td><span class="dot-label bg-danger" title="Приглашение не отправлено"></span></td>'
                    }
                    html += '<td>' + employee_name + '</td>'
                    html += '<td>' + employee_email + '</td>'
                    html += '<td>' + employee_invitation_sent_datetime + '</td>'
                    html += '<td>' +
                        '<div style="text-align: center;" >' +
                            '<i class="fe fe-more-vertical cursor-pointer" data-bs-toggle="dropdown" aria-expanded="false" style="font-size: 20px"></i>' +
                            '<ul class="dropdown-menu">'
                    if(employee_invitation){
                        html += '<li><a class="dropdown-item details cursor-pointer">Подробно</a></li>'
                    }else {
                        html += '<li><a class="dropdown-item send-email-invitation cursor-pointer">Отправить приглашение</a></li>'
                    }
                    html += '</ul>' +
                        '</div>' +
                        '</td>'
                    html += '</tr>'

                })
                $('#tbody_participants_selected').html(html)
                $('#modal_participants').modal('hide')
                btn_text($('#save_participants'), 'Сохранить')
                toastr.success('Участники добавлены')

            }
        });



    }


})

$('#tbody_participants_selected').on('click', '.send-email-invitation', function () {

    let participant_id = $(this).closest('tr').attr('id').split('_')[2]
    let question_groups = []

    let output_html = '<hr class="solid mt-0" style="background-color: black;">' +
                    '<div>Отправить приглашение участнику?</div>' +
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
            headers: { "X-CSRFToken": token },
            url: url_send_invitation_email,
            type: 'POST',

            data: JSON.stringify({
                                'study_id': study_id,
                                'participant_id': participant_id,
                                'question_groups': question_groups,
                                'type': 'initial'

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
                    let datetime_invitation_sent = json_data['datetime_invitation_sent'];
                    let el = $('#participant_id_' + participant_id)
                    el.find('.bg-danger').removeClass('bg-danger').addClass('bg-warning').prop('title', 'Приглашение отправлено')
                    el.find('.send-email-invitation').text('Повторно отправить приглашение')
                    el.find('td:nth-child(4)').text(datetime_invitation_sent)
                    toastr.success('Приглашение участнику отправлено')

                }

                hide_progressbar_loader()

            }
        });




      }
    })
})
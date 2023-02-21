expand_menu_item('#menu_employees_list')
    let employee_id
    $('#save_edited_employee').on('click', function (){

        let name = $('#employee_name').val()
        let email = $('#employee_email').val()
        let role = $('#employee_role').val()
        let position = $('#employee_position').val()
        let industry = $('#employee_industry').val()
        let gender = $('#employee_gender').val()
        let employee_birth_year = $('#employee_birth_year').val()
        if (email === '' || role === '' || position === '' || industry === ' ' || gender === '' || employee_birth_year === ''){
            toastr.error('Все поля, кроме имени, должны быть заполнены')
        }else {
            if(!isEmail(email)) {
                toastr.error('Указан некорректный email')
            }else {
                btn_spinner($('#save_edited_employee'))

                let role_id = $('#employee_role').children(':selected').prop('id')
                let position_id = $('#employee_position').children(':selected').prop('id')
                let industry_id = $('#employee_industry').children(':selected').prop('id')

                let data = {
                        'name': name,
                        'role_id': role_id,
                        'email': email,
                        'position_id': position_id,
                        'industry_id': industry_id,
                        'gender': gender,
                        'employee_birth_year': employee_birth_year,
                        'employee_id': employee_id

                }
                console.log(data)
                        $.ajax({
                            headers: { "X-CSRFToken": token },
                            url: url_save_new_employee_html,
                            type: 'POST',
                            data: JSON.stringify({
                                        'employee_data': data,
                                    }),
                            processData: false,
                            contentType: false,
                            error: function(data){
                                toastr.error('Ошибка', data)
                            },
                            success:function (data) {
                                console.log(data)
                                let output_html
                                if(data === 'email exists'){
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

                                }else {
                                    output_html = '<hr class="solid mt-0" style="background-color: black;">' +
                                                    '<div>Данные сотрудника изменены' + '</div>' +
                                                    '<br>' +
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

                                btn_text($('#save_edited_employee'), 'Сохранить')
                            }
                        });



            }


        }
    })


    $('#main-container').on('click', '.edit-employee', function () {
        employee_id = $(this).closest('tr').attr('id').split('_')[2]
        show_progressbar_loader()

        $.ajax({
            headers: { "X-CSRFToken": token },
            url: url_get_employee_data,
            type: 'POST',

            data: JSON.stringify({
                        'employee_id': employee_id,
                    }),
            processData: false,
            contentType: false,
            error: function(data){
                toastr.error('Ошибка', data)
            },
            success:function (data) {
                hide_progressbar_loader()
                console.log(data)
                if (!server_error){
                    $('#employee_role option').each(function (e) {
                        if(data['role']['id'] === $(this).prop('id')){
                            $(this).prop('selected', true)
                        }
                    })
                    $('#employee_position option').each(function (e) {
                        if(data['position']['id'] === $(this).prop('id')){
                            $(this).prop('selected', true)
                        }
                    })
                    $('#employee_industry option').each(function (e) {
                        if(data['industry']['id'] === $(this).prop('id')){
                            $(this).prop('selected', true)
                        }
                    })
                    $('#employee_gender option').each(function (e) {
                        if(data['gender']['id'] === $(this).prop('id')){
                            $(this).prop('selected', true)
                        }
                    })
                }else {
                    let role = data['role']
                    let position = data['position']
                    let industry = data['industry']
                    let gender = data['gender']

                    $('#employee_role').html('<option id="' + role['id'] + '">' + role['name_ru'] + '</option>')
                    $('#employee_position').html('<option id="' + position['id'] + '">' + position['name_ru'] + '</option>')
                    $('#employee_industry').html('<option id="' + industry['id'] + '">' + industry['name_ru'] + '</option>')
                    $('#employee_gender').html('<option id="' + gender['id'] + '">' + gender['name_ru'] + '</option>')
                }
                $("#employee_birth_year").val(data['birth_year']).yearpicker({
                    // onChange: function (val) {
                    //     console.log(val)
                    // },
                    year: data['birth_year'],
                    startYear: 1940,
                    endYear: 2010,
                })
                $("#employee_name").val(data['name'])
                $("#employee_email").val(data['email'])
            }
        });
        $('#modal_edit_imployee').modal('show')
    })
    $('#main-container').on('click', '.delete-employee', function () {
        let employee_tr_id = $(this).closest('tr').attr('id')
        let employee_name = $(this).closest('tr').find('td').eq(0).text()

        let output_html = '<hr class="solid mt-0" style="background-color: black;">' +
                        '<div>Удалить сотудника?</div>' +
                        '<div><b>' + employee_name + '</b></div>' +
                        '<br>' +
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
          if (result.isConfirmed) {
            employee_id = $(this).closest('tr').attr('id').split('_')[2]

            show_progressbar_loader()

            $.ajax({
                headers: { "X-CSRFToken": token },
                url: url_delete_employee,
                type: 'POST',

                data: JSON.stringify({
                            'employee_id': employee_id,
                        }),
                processData: false,
                contentType: false,
                error: function(data){
                    toastr.error('Ошибка', data)
                },
                success:function (data) {
                    hide_progressbar_loader()

                    if('errors' in data){
                        output_html = ''
                        let list_html = '<ul><hr class="solid" style="background-color: black;">'
                        for(let i=0; i < data['errors'].length; i++){
                            console.log(data['errors'][i])

                            list_html += '<li style="text-align: left; padding-left: 7px;"><b>'
                            list_html += '- ' + data['errors'][i]
                            list_html += '</b></li>'
                        }
                        list_html += '</ul>'
                        output_html = '<div>Сотрудник не может быть удален по следующим причинам:' +
                                         list_html +
                                        '</div>'
                        Swal.fire({
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



                    }else {
                        $('#' + employee_tr_id).remove()
                        toastr.success('Сотрудник удален')
                    }


                }
            });
          }
        })


    })


    let company_id

    function route_menu_handler(route_index, btn_type) {
        let new_menu_number = 0
        if(btn_type === 'next'){
            new_menu_number = route_index + 1
        }else {
            new_menu_number = route_index - 1
        }
        console.log('new_menu_number - ' + new_menu_number)
            $('.route-item').each(function (i, obj) {
                if(parseInt($(this).find('.number').html()) !== new_menu_number){
                    $(this).addClass('disabled')
                    $(this).removeClass('current')

                }else {
                    $(this).removeClass('disabled')
                    $(this).addClass('current')
                }
            })
            if(new_menu_number === 3){
                // {#$('#next').addClass('disabled')#}
                // {#$('#next').removeClass('cursor-pointer')#}
            }else {
                $('#next').removeClass('disabled')

            }

    }


    function route_handler(route_index) {
    // console.log('project - ' + $('.project-chosen').text().trim())
    //     console.log('route_index - ' + route_index)
        btn_spinner($('#next'))
        switch (route_index) {
            case 1:
                let company_id = $('.project-chosen').attr('id').split('_')[2]
                $.ajax({
                    headers: { "X-CSRFToken": token },
                    url: url_get_company_employees,
                    type: 'POST',

                    data: JSON.stringify({
                                'company_id': company_id,
                            }),
                    processData: false,
                    contentType: false,
                    error: function(data){
                        toastr.error('Ошибка', data)
                    },
                    success:function (data) {
                        console.log(data)
                        // {#let data_json = $.parseJSON(data);#}
                        let data_json = data['data'];
                        let name = ''
                        let html = ''
                        for(let i=0; i < data_json.length; i++){
                            if(data_json[i]['name'] === 'null'){
                                name = ''
                            }else {
                                name = data_json[i]['name']
                            }
                            html += '<tr class="" id=employee_id_' + data_json[i]['id'] + '>'
                            html += '<td>' + data_json[i]['name'] + '</td>'
                            html += '<td>' + data_json[i]['email'] + '</td>'
                            html += '<td>' + data_json[i]['industry'] + '</td>'
                            html += '<td>' + data_json[i]['role'] + '</td>'
                            html += '<td>' + data_json[i]['position'] + '</td>'
                            html += '<td>' + data_json[i]['birth_year'] + '</td>'
                            html += '<td>' + data_json[i]['sex'] + '</td>'
                            html += '<td>' + data_json[i]['created_at'] + '</td>'
                            html += '<td>' + data_json[i]['created_by'] + '</td>'
                            html += '<td>'
                            html += '<div style="text-align: center;">'
                            html += '<i class="fe fe-more-vertical cursor-pointer" data-bs-toggle="dropdown" aria-expanded="false" style="font-size: 20px"></i>'
                            html += '<ul class="dropdown-menu">'
                            html += '<li><a class="dropdown-item edit-employee cursor-pointer">Изменить</a></li>'
                            if($('#cur_role_name').text() === 'Менеджер' || $('#cur_role_name').text() === 'Админ заказчика'){
                                console.log(data_json[i]['created_by_email'])
                                if(cur_user_email === data_json[i]['created_by_email']){
                                    html += '<li><a class="dropdown-item cursor-pointer delete-employee">Удалить</a></li>'
                                }
                            }else {
                                html += '<li><a class="dropdown-item cursor-pointer delete-employee">Удалить</a></li>'
                            }
                            html += '</ul>'
                            html += '</div>'

                            html += '</td>'

                            html += '</tr>'


                        }
                        // {#console.log(html)#}
                        $('#wizard1-tbody-1').html(html)
                        // {#console.log('wizard1-tbody-1 - ' + $('#wizard1-tbody-1').html())#}
                        process_table('.team-table')
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
    $(".table-row").on('click', function (e) {
        $(".table-row").css('background-color', '').css('color', '').removeClass('project-chosen')
        $(this).css('background-color', '#6c5ffc').css('color', 'white').addClass('project-chosen')
        $('#next').removeClass('disabled')
    })

    $('#next').on('click', function () {
        if ($(this).hasClass('disabled')){
            if(enabled_route_number === 1){
                toastr.error('Выберите проект')
            }
        }else {
            // {#$(this).find('a').html('<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true" style="width: 25px;height: 25px;"></span>')#}
            $('.route-item').each(function (i, obj) {
                if(!$(this).hasClass('disabled')){
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
            if(!$(this).hasClass('disabled')){
                enabled_route_number = parseInt($(this).find('.number').html())

            }
                // {#route_menu_handler($(this).find('.number').html())#}

        })
        switch (enabled_route_number){
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
    function process_table(element){
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

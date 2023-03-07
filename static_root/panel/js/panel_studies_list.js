expand_menu_item('#menu_study_list')

    let study_id

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
                let role_id = $('#employee_role option:selected').val().split('_')[2]
                let position_id = $('#employee_position option:selected').val().split('_')[2]
                let industry_id = $('#employee_industry option:selected').val().split('_')[2]

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


    $('#main-container').on('click', '.study-details', function () {
        let study_id = $(this).closest('tr').data('study-id')
        window.location.href = 'study/' + study_id
    });

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
        console.log('route_index - ' + route_index)
        btn_spinner($('#next'))
        switch (route_index) {
            case 1:
                let company_id = $('.company-chosen').attr('id').split('_')[2]
                $.ajax({
                    headers: { "X-CSRFToken": token },
                    url: url_get_company_studies,
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
                            html += `<tr class="" id="${data_json[i]['id']}" data-study-id="${data_json[i]['id']}">`
                            html += '<td>' + data_json[i]['name'] + '</td>'
                            html += '<td>' + data_json[i]['company_name'] + '</td>'
                            html += '<td>' + data_json[i]['research_name'] + '</td>'
                            html += '<td>'
                            html += '<div style="text-align: center;">'
                            html += '<i class="fe fe-more-vertical cursor-pointer" data-bs-toggle="dropdown" aria-expanded="false" style="font-size: 20px"></i>'
                            html += '<ul class="dropdown-menu">'
                            html += '<li><a class="dropdown-item study-details cursor-pointer">Подробно</a></li>'
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
    // выбор компании
    $(".table-row").on('click', function (e) {
        $(".table-row").css('background-color', '').css('color', '').removeClass('company-chosen')
        $(this).css('background-color', '#6c5ffc').css('color', 'white').addClass('company-chosen')
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
          "paging": true,
          "language": {
            "url": "//cdn.datatables.net/plug-ins/9dcbecd42ad/i18n/Russian.json"
          },
          "initComplete": function () {

          },
        })
    }

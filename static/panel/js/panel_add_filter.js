expand_menu_item('#menu_filters_list')

$('#default_filter').on('click', function () {
    console.log($(this).prop('checked'))
    if ($(this).prop('checked')) {

        $('#filter_params_block').hide()
    } else {
        $('#filter_params_block').show()
    }
})

// if (default_filters_cnt === 0) {
//     $('#default_filter').prop('checked', true).prop('disabled', true)
//     $('#filter_params_block').hide()
//
// }

let save_filter_clicked = false
$('#save_filter').on('click', function () {
    save_filter_clicked = true
    let filter_data = []
    let is_default = $('#default_filter').prop('checked')
    let filter_params_ok = true
    let tpoint_ok = true
    btn_spinner($('#save_filter'))
    let input_filter_name = $('#input_filter_name').val()
    let select_industry = $('#select_industry').val()
    let select_position = $('#select_position').val()
    let select_role = $('#select_role').val()
    let gender_year = $('#select_age_gender').val()
    let industry_id, position_id, role_id, age_gender_id

    if (input_filter_name === '' || gender_year === '-- Сделайте выбор --') {
        filter_params_ok = false
        toastr.error('Имя и Пол-Возраст должны быть заполнены')
        btn_text($('#save_filter'), 'Сохранить фильтр')
    }
    if (!is_default) {


        if (select_industry === '-- Сделайте выбор --' || select_position === '-- Сделайте выбор --' || select_role === '-- Сделайте выбор --') {
            filter_params_ok = false
            toastr.error('Все параметры должны быть заполнены')
            btn_text($('#save_filter'), 'Сохранить фильтр')

        } else {
            industry_id = $('#select_industry option:selected').val()
            position_id = $('#select_position option:selected').val()
            role_id = $('#select_role option:selected').val()
            age_gender_id = $('#select_age_gender option:selected').val()
        }
    }


    $('.tpoint').each(function () {
        let t_point = $(this).val()
        let category_id = $(this).attr('data-category-id')
        let raw_point = $(this).attr('data-raw-point')
        // console.log(`category_id - ${category_id} raw_point - ${raw_point} t_point - ${t_point} `)
        if (t_point === '') {
            $(this).css('background-color', 'red')
            tpoint_ok = false
        } else {
            filter_data.push({
                'category_id': category_id,
                'raw_points': raw_point,
                't_points': t_point,
            })
        }
    })

    if (!tpoint_ok) {
        toastr.error('Все баллы должны быть заполнены')
        btn_text($('#save_filter'), 'Сохранить фильтр')

    }
    if (filter_params_ok && tpoint_ok) {
        // if (filter_params_ok) {
        btn_spinner($('#save_filter'))
        $.ajax({
            headers: {"X-CSRFToken": token},
            url: url_save_new_filter,
            type: 'POST',
            data: JSON.stringify({
                'industry_id': industry_id,
                'position_id': position_id,
                'role_id': role_id,
                'age_gender_id': age_gender_id,
                'filter_data': filter_data,
                'is_default': is_default,
                'name': input_filter_name,
            }),
            processData: false,
            contentType: false,
            error: function (data) {
                toastr.error('Ошибка', data)
            },
            success: function (data) {
                btn_text($('#save_filter'), 'Сохранить фильтр')
                // hide_progressbar_loader()
                // let employees = data['response']['employees']
                Swal.fire({
                    title: 'Данные сохранены',
                    text: "Исследование добавлено",
                    icon: 'success',
                    confirmButtonColor: '#3085d6',
                    cancelButtonColor: '#d33',
                    confirmButtonText: 'ОК'
                })

            }
        })

    }
})
$('.tpoint').on('click', function () {
    if (save_filter_clicked) {
        $('.tpoint').css('background-color', 'white')
        save_filter_clicked = false
    }
})

let sheets_data = []

let ExcelToJSON = function () {

    this.parseExcel = function (file) {
        let reader = new FileReader();

        reader.onload = function (e) {
            let data = e.target.result;
            let workbook = XLSX.read(data, {
                type: 'binary'
            });
            workbook.SheetNames.forEach(function (sheetName) {
                // Here is your object
                let XL_row_object = XLSX.utils.sheet_to_row_object_array(workbook.Sheets[sheetName]);
                let json_object = JSON.stringify(XL_row_object);
                sheets_data.push(json_object)
                // console.log(sheetName);
                // console.log(json_object);

            })
            // console.log('sheets_data')
            // console.log(sheets_data[0])
            send_file_data($.parseJSON(sheets_data[0]))

        };

        reader.onerror = function (ex) {
            console.log(ex);
        };

        reader.readAsBinaryString(file);
        // return sheets_data[0]

    };

};

$('#save_filter_file').on('click', function () {
    sheets_data = []
    let files = $('#input_filter_file').prop('files');
    console.log(files.length)
    if (files.length === 0) {
        toastr.error('Выберите файл')
    } else {
        let xl2json = new ExcelToJSON();
        xl2json.parseExcel(files[0]);
    }
})

function send_file_data(data) {
    // console.log(data)
    let data_ok = true
    data.forEach(function (row) {
        console.log(Object.keys(row).length)
        if (Object.keys(row).length < 38) {
            toastr.error('В файле не хватает данных')
            data_ok = false
            // let control = $("#input_filter_file");
            // control.replaceWith( control = control.clone( true ) );
            // const form = document.getElementById('input_filter_file');
            // form.reset();
            // $("#input_filter_file_form")[0].reset()
            // $("#input_filter_file").val('')
            // $("#input_filter_file").replaceWith($("#input_filter_file").clone(true))

        }
    })
    $("#input_filter_file").val('')
    let clone = $("#input_filter_file").clone(true)
    $("#input_filter_file").replaceWith(clone)

    if (data_ok) {
        save_filter_clicked = true
        let is_default = $('#default_filter').prop('checked')
        let filter_params_ok = true
        btn_spinner($('#save_filter_file'))
        let input_filter_name = $('#input_filter_name').val()
        let select_industry = $('#select_industry').val()
        let select_position = $('#select_position').val()
        let select_role = $('#select_role').val()
        let gender_year = $('#select_age_gender').val()
        let industry_id, position_id, role_id, age_gender_id

        if (input_filter_name === '' || gender_year === '-- Сделайте выбор --') {
            filter_params_ok = false
            toastr.error('Имя и Пол-Возраст должны быть заполнены')
            btn_text($('#save_filter_file'), 'Сохранить файл фильтр')

        }
        if (!is_default) {


            if (select_industry === '-- Сделайте выбор --' || select_position === '-- Сделайте выбор --' || select_role === '-- Сделайте выбор --') {
                filter_params_ok = false
                toastr.error('Все параметры должны быть заполнены')
                btn_text($('#save_filter_file'), 'Сохранить файл фильтр')

            } else {
                industry_id = $('#select_industry option:selected').val()
                position_id = $('#select_position option:selected').val()
                role_id = $('#select_role option:selected').val()
            }
        }

        if (filter_params_ok) {
            // if (filter_params_ok) {
            age_gender_id = $('#select_age_gender option:selected').val()

            btn_spinner($('#save_filter_file'))
            $.ajax({
                headers: {"X-CSRFToken": token},
                url: url_save_new_filter_from_file,
                type: 'POST',
                data: JSON.stringify({
                    'industry_id': industry_id,
                    'position_id': position_id,
                    'role_id': role_id,
                    'age_gender_id': age_gender_id,
                    'filter_data': data,
                    'is_default': is_default,
                    'name': input_filter_name,
                }),
                processData: false,
                contentType: false,
                error: function (data) {
                    toastr.error('Ошибка', data)
                },
                success: function (data) {
                    btn_text($('#save_filter_file'), 'Сохранить файл фильтр')

                    if (data['error']) {
                        console.log(data['error'])
                        // hide_progressbar_loader()
                        let output_html = '<hr class="solid mt-0" style="background-color: black;">'

                        if(data['error']['wrong_codes']){
                            output_html = output_html + '<div>Следующие коды категорий отсутствуют:</div>'
                            data['error']['wrong_codes'].forEach(function (code) {
                                output_html = output_html + '<div><b>' + code + '</b></div>'
                            })
                            output_html = output_html + '<br><hr class="solid mt-0" style="background-color: black;">'
                        }
                        if(data['error']['filter_exists']) {
                            output_html = output_html + '<div>Фильтр с выбранными параметр существует</div>' +
                                '<br>' +
                                '<hr class="solid mt-0" style="background-color: black;">'
                        }
                        Swal.fire({
                            html: output_html,
                            icon: 'error',
                            confirmButtonColor: '#3085d6',
                            cancelButtonColor: '#d33',
                            confirmButtonText: 'ОК'
                        })

                    }else {
                        Swal.fire({
                            title: 'Данные сохранены',
                            text: "Фильтр добавлен",
                            icon: 'success',
                            confirmButtonColor: '#3085d6',
                            cancelButtonColor: '#d33',
                            confirmButtonText: 'ОК'
                        })

                    }

                }
            })

        }


    }

}

// $('#select_company').on("select2:select", function(e) {
//     let company_active = $('#select_company :selected').attr('data-company-active')
//     if(company_active === 'True'){
//         $('#company_active').prop('checked', 'checked')
//     }else {
//         $('#company_active').prop('checked', '')
//     }
//     $('#table_participants_for_study').DataTable().destroy()
//     $('#tbody_participants_selected').html('')
//      process_table_clear('#table_participants_for_study')
// });
//
// $('#save_study').on('click', function () {
//     let employees_ids = []
//     let company_id = $('#select_company :selected').attr('id').split('_')[2]
//     let test_ok = true
//     $('#tbody_participants_selected tr').each(function () {
//         employees_ids.push($(this).attr('data-employee-id'))
//     })
//     if(employees_ids.length === 0 || $('#tbody_participants_selected tr .dataTables_empty').length === 1){
//         test_ok = false
//         toastr.error('Список участников исследования пуст')
//     }
//     let template_id = $('#select_template :selected').val()
//     if(template_id === ''){
//         test_ok = false
//         toastr.error('Необходимо выбрать шаблон')
//
//     }
//     let input_study_name = $('#input_study_name').val()
//     if(input_study_name === ''){
//         test_ok = false
//         toastr.error('Название должно быть заполнено')
//
//     }
//
//     if(test_ok){
//         btn_spinner('#save_study')
//         $.ajax({
//             headers: {"X-CSRFToken": token},
//             url: url_add_new_study,
//             type: 'POST',
//             data: JSON.stringify({
//                 'template_id': template_id,
//                 'employees_ids': employees_ids,
//                 'input_study_name': input_study_name,
//                 'company_id': company_id,
//             }),
//             processData: false,
//             contentType: false,
//             error: function (data) {
//                 toastr.error('Ошибка', data)
//             },
//             success: function (data) {
//                 btn_text('#save_study', 'Сохранить исследование')
//                 // hide_progressbar_loader()
//                 // let employees = data['response']['employees']
//                 Swal.fire({
//                   title: 'Данные сохранены',
//                   text: "Исследование добавлено",
//                   icon: 'success',
//                   confirmButtonColor: '#3085d6',
//                   cancelButtonColor: '#d33',
//                   confirmButtonText: 'ОК'
//                 })
//
//             }
//         })
//
//
//     }
//
//
//
// })
//
//
// $('#add_participants').on('click', function () {
//     let company_id = $('#select_company').val()
//     let company_id_is_empty = false
//     if(company_id === ''){
//         company_id_is_empty = true
//     }
//
//     if(!company_id_is_empty){
//         // $('#modal_add_participant')
//         // $('#tbody_participants_to_choose').html('')
//         show_progressbar_loader()
//         $.ajax({
//             headers: { "X-CSRFToken": token },
//             url: url_get_company_employees_for_new_study,
//             type: 'POST',
//             data: JSON.stringify({
//                 'company_id': company_id,
//             }),
//             processData: false,
//             contentType: false,
//             error: function(data){
//                 toastr.error('Ошибка', data)
//             },
//             success:function (data) {
//                 hide_progressbar_loader()
//                 let employees = data['response']['employees']
//                 // console.log(employees)
//                 // process_table('.team-table')
//                 let participants_already_added_ids = []
//                 $('#tbody_participants_selected tr').each(function () {
//                     participants_already_added_ids.push($(this).attr('data-employee-id'))
//                 })
//                 console.log(participants_already_added_ids)
//                 $('#modal_add_participant').DataTable().destroy()
//                 $('#tbody_participants_to_choose').html('')
//                 employees.forEach(function (employee) {
//                     console.log(employee)
//                     console.log($.inArray(employee['id'], participants_already_added_ids))
//                     if($.inArray(employee['id'].toString(), participants_already_added_ids) === -1){
//                         let html = `<tr id="employee_id_${employee['id']}">` +
//                             '         <td>\n' +
//                             '            <input type="checkbox" class="" name="example-checkbox1" value="option1" style="transform: scale(1.1)">\n' +
//                             `         </td>\n` +
//                             `         <td>${employee['name']}</td>` +
//                             `         <td>${employee['email']}</td>` +
//                             `         <td>${employee['industry']}</td>` +
//                             `         <td>${employee['role']}</td>` +
//                             `         <td>${employee['position']}</td>` +
//                             `         <td>${employee['birth_year']}</td>` +
//                             `         <td>${employee['sex']}</td>` +
//                             `        </tr>`
//                         $('#tbody_participants_to_choose').append(html)
//
//                     }
//                 })
//                 process_table_clear('#modal_add_participant')
//             }
//         });
//
//         $('#check_all_employees_for_study').prop('checked', '')
//         $('#modal_participants').modal('show')
//     }else {
//         Swal.fire({
//           title: 'Данные отсутствуют',
//           text: "Компания должна быть выбрана",
//           icon: 'warning',
//           confirmButtonColor: '#3085d6',
//           cancelButtonColor: '#d33',
//           confirmButtonText: 'ОК'
//         })
//
//     }
// })
//
// $('#check_all_employees_for_study').on('click', function () {
//     console.log($(this).prop('checked'))
//         if($(this).prop('checked') === true){
//             $('#tbody_participants_to_choose input').each(function (index) {
//                 $(this).prop('checked', 'checked')
//             })
//         }else {
//             $('#tbody_participants_to_choose input').each(function (index) {
//                 $(this).prop('checked', '')
//             })
//
//         }
//
// })
//
// $('#add_participants_to_study').on('click', function () {
//     let html_for_study_list
//     let row_html
//     $('#tbody_participants_to_choose tr').each(function (index) {
//         if($(this).find('input').prop('checked') === true){
//             let id = $(this).attr('id').split('_')[2]
//             let name = $(this).find('td').eq(1).text()
//             let email = $(this).find('td').eq(2).text()
//             let industry = $(this).find('td').eq(3).text()
//             let role = $(this).find('td').eq(4).text()
//             let position = $(this).find('td').eq(5).text()
//             let birth_year = $(this).find('td').eq(6).text()
//             let sex = $(this).find('td').eq(7).text()
//             row_html = `<tr data-employee-id="${id}">` +
//                         `<td>${name}</td>` +
//                         `<td>${email}</td>` +
//                         `<td>${industry}</td>` +
//                         `<td>${role}</td>` +
//                         `<td>${position}</td>` +
//                         `<td>${birth_year}</td>` +
//                         `<td>${sex}</td>` +
//                         `<td><i class="fe fe-x remove-participant-from-study" style="font-size: 18px; cursor: pointer" title="Удалить"></i></td>` +
//                         `</tr>`
//             html_for_study_list = html_for_study_list + row_html
//         }
//     })
//     $('#table_participants_for_study').DataTable().destroy()
//     $('#tbody_participants_selected').append(html_for_study_list)
//      process_table_clear('#table_participants_for_study')
//     $('#modal_participants').modal('hide')
// })
//
// $('#tbody_participants_selected').on('click', '.remove-participant-from-study', function () {
//     console.log('rrrrr')
//     $('#table_participants_for_study').DataTable().destroy()
//     $(this).closest('tr').remove()
//     process_table_clear('#table_participants_for_study')
//
// })
//


//
// function process_circle_progress(){
//     $('svg.radial-progress').each(function( index, value ) {
//         // If svg.radial-progress is approximately 25% vertically into the window when scrolling from the top or the bottom
//             // Get percentage of progress
//             let percent = $(value).data('percentage');
//             // Get radius of the svg's circle.complete
//             let radius = $(this).find($('circle.complete')).attr('r');
//             // Get circumference (2πr)
//             let circumference = 2 * Math.PI * radius;
//             // Get stroke-dashoffset value based on the percentage of the circumference
//             let strokeDashOffset = circumference - ((percent * circumference) / 100);
//             // Transition progress for 1.25 seconds
//             $(this).find($('circle.complete')).animate({'stroke-dashoffset': strokeDashOffset}, 1250);
//             // if(percent === 100){
//             //
//             // }
//
//         });
// }
//
// process_circle_progress()
//
// $('#tbody_participants_selected').on('click', '.add-question-groups', function () {
//     show_progressbar_loader()
//     let html = ''
//     let participant_tr_id = $(this).closest('tr').attr('id')
//     let participant_tr_p = $('#' + participant_tr_id).find('.participant_selected_questions_groups_td p')
//     $('#tbody_question_groups_selected tr').each(function () {
//         let questions_group_code_modal = $(this).attr('id').split('_')[2]
//         let question_exists = false
//
//         participant_tr_p.each(function () {
//             let questions_group_code_participant_selected = $(this).attr('id').split('_')[5]
//             if(questions_group_code_modal === questions_group_code_participant_selected){
//                 question_exists = true
//             }
//         })
//         if(question_exists){
//             html += '<tr class="question_group_item question_group_selected cursor-pointer" id="modal' + $(this).attr("id") + '">'
//         }else {
//             html += '<tr class="question_group_item cursor-pointer" id="modal' + $(this).attr("id") + '">'
//         }
//
//         html += '<td>' + $(this).children('td').eq(0).text() + '</td>'
//         html += '<td></td>'
//         html += '</tr>'
//
//     })
//     let el = $('#tbody_modal_questions_groups')
//     el.html(html)
//     el.attr('data-participant-tr-id', participant_tr_id)
//
//     hide_progressbar_loader()
//     $('#modal_question_groups').modal('show')
// })
//
// $('#tbody_modal_questions_groups').on('click', '.question_group_item', function(){
//     if($(this).hasClass('question_group_selected')){
//         $(this).removeClass('question_group_selected')
//     }else {
//         $(this).addClass('question_group_selected')
//     }
// })
//
// $('#select_all_question_groups').on('click', function () {
//     if ($(this).attr('checked') === 'checked'){
//         $(this).attr('checked', false)
//         $('#tbody_modal_questions_groups').find('.question_group_item').each(function () {
//             $(this).removeClass('question_group_selected')
//         })
//         // active = 0
//     }else {
//         $(this).attr('checked', 'checked')
//         $('#tbody_modal_questions_groups').find('.question_group_item').each(function () {
//             $(this).addClass('question_group_selected')
//         })
//
//         // active = 1
//     }
// })
//
// $('#save_question_groups').on('click', function () {
//     let questions_groups_selected = []
//
//     $('#tbody_modal_questions_groups').find('.question_group_selected').each(function () {
//         let code = $(this).attr('id').split('_')[2]
//         questions_groups_selected.push({
//             'name': $(this).find('td').text(),
//             'code': code
//         })
//     })
//     if(questions_groups_selected.length === 0){
//         toastr.error('Выберите группу(ы) вопросов')
//     }else {
//         let participant_tr_id = $('#tbody_modal_questions_groups').attr('data-participant-tr-id')
//         let participant_id = participant_tr_id.split('_')[2]
//         let data = {
//             'questions_groups_selected': questions_groups_selected,
//             'participant_id': participant_id,
//         }
//         btn_spinner($('#save_question_groups'))
//         $.ajax({
//             headers: { "X-CSRFToken": token },
//             url: url_save_participant_questions_groups,
//             type: 'POST',
//
//             data: JSON.stringify({
//                             'data': data,
//                             'study_id': study_id
//                         }),
//             processData: false,
//             contentType: false,
//             error: function(data){
//                 toastr.error('Ошибка', data)
//             },
//             success:function (data) {
//                 let role_name = $('#cur_role_name').text()
//                 console.log(data)
//                 let data_json = data['response']
//                 if(data_json === 'logout'){
//                     window.location.href = url_login_home
//                 }else {
//                     if (data_json === 'company_deactivated' && role_name === 'Админ заказчика') {
//                         $('#modal_question_groups').modal('hide')
//                         btn_text($('#save_question_groups'), 'Сохранить')
//
//                         let output_html = '<hr class="solid mt-0" style="background-color: black;">' +
//                             '<div>Компания деактивирована' + '</div>' +
//                             '<div>Если Вы не знаете причин - обратитесь к менеджеру' + '</div>' +
//                             '<br>' +
//                             '<hr class="solid mt-0" style="background-color: black;">'
//                         Swal.fire({
//                             html: output_html,
//                             icon: 'warning',
//                             confirmButtonColor: '#3085d6',
//                             cancelButtonColor: '#d33',
//                             confirmButtonText: 'ОК'
//                         })
//                     } else {
//                         if (data['warning']) {
//                             toastr.warning(data['warning'])
//                         }
//
//
//                         let html = ''
//                         for (let i = 0; i < questions_groups_selected.length; i++) {
//                             let questions_group_selected = questions_groups_selected[i]
//                             html += '<p class="mb-0 participant-selected-question-group" id="participant_selected_question_group_id_' + questions_group_selected['code'] + '">' + questions_group_selected['name'] + '</p>'
//                         }
//                         let el = $('#' + participant_tr_id).find('.participant_selected_questions_groups_td')
//                         el.html('')
//                         el.html(html)
//                         $('#modal_question_groups').modal('hide')
//                         btn_text($('#save_question_groups'), 'Сохранить')
//                         toastr.success('Группы вопросов сохранены')
//
//
//                     }
//
//                 }
//
//
//
//             }
//         });
//
//
//
//     }
//
//
// })
//
//
// $('#add_participant').on('click', function () {
//     show_progressbar_loader()
//     $.ajax({
//         headers: { "X-CSRFToken": token },
//         url: url_get_employees_for_study,
//         type: 'POST',
//
//         data: JSON.stringify({
//                             'study_id': study_id
//                         }),
//         processData: false,
//         contentType: false,
//         error: function(data){
//             toastr.error('Ошибка', data)
//         },
//         success:function (data) {
//             let role_name = $('#cur_role_name').text()
//             console.log(data)
//             hide_progressbar_loader()
//             let data_json = data['response']
//             if(data_json === 'logout'){
//                 window.location.href = url_login_home
//             }else {
//                 if(data_json === 'None'){
//
//                     let output_html = '<hr class="solid mt-0" style="background-color: black;">' +
//                                     '<div>Cотрудники для распределения отсутстуют' + '</div>' +
//                                     '<br>' +
//                                     '<hr class="solid mt-0" style="background-color: black;">'
//                     Swal.fire({
//                       html: output_html,
//                       icon: 'warning',
//                       confirmButtonColor: '#3085d6',
//                       cancelButtonColor: '#d33',
//                       confirmButtonText: 'ОК'
//                     })
//                 }else{
//                     if (data_json === 'company_deactivated' && role_name === 'Админ заказчика'){
//                         let output_html = '<hr class="solid mt-0" style="background-color: black;">' +
//                                         '<div>Компания деактивирована' + '</div>' +
//                                         '<div>Если Вы не знаете причин - обратитесь к менеджеру' + '</div>' +
//                                         '<br>' +
//                                         '<hr class="solid mt-0" style="background-color: black;">'
//                         Swal.fire({
//                           html: output_html,
//                           icon: 'warning',
//                           confirmButtonColor: '#3085d6',
//                           cancelButtonColor: '#d33',
//                           confirmButtonText: 'ОК'
//                         })
//                     }else {
//                         if(data['warning']){
//                             toastr.warning(data['warning'])
//                         }
//                         let html = ''
//                         for(let i=0; i < data_json.length; i++) {
//                             console.log('id - ' + data_json[i]['participant_id'] + 'len - ' + $('#tbody_participants_selected').find('#participant_id_' + data_json[i]['participant_id']).length)
//                             if($('#tbody_participants_selected').find('#participant_id_' + data_json[i]['participant_id']).length > 0){
//                                 html += '<tr class="participant_item participant_item_selected cursor-pointer" id="employee_id_' + data_json[i]['employee_id'] + '">'
//                             }else {
//                                 html += '<tr class="participant_item  cursor-pointer" id="employee_id_' + data_json[i]['employee_id'] + '">'
//                             }
//                             html += '<td class=" employee-name">' + data_json[i]['name'] + '</td>'
//                             html += '<td class="text-end employee-email">' + data_json[i]['email'] + '</td>'
//                             html += '</tr>'
//                         }
//                         $('#tbody_modal_participants').html(html)
//                         $('#modal_participants').modal('show')
//                     }
//
//                 }
//             }
//         }
//     });
//
//
// })
//
// $('#select_all_participants').on('click', function () {
//     if ($(this).attr('checked') === 'checked'){
//         $(this).attr('checked', false)
//         $('#tbody_modal_participants').find('.participant_item').each(function () {
//             $(this).removeClass('participant_item_selected')
//         })
//         // active = 0
//     }else {
//         $(this).attr('checked', 'checked')
//         $('#tbody_modal_participants').find('.participant_item').each(function () {
//             $(this).addClass('participant_item_selected')
//         })
//
//         // active = 1
//     }
// })
//
// $('#tbody_modal_participants').on('click', '.participant_item', function(){
//     if($(this).hasClass('participant_item_selected')){
//         $(this).removeClass('participant_item_selected')
//     }else {
//         $(this).addClass('participant_item_selected')
//     }
// })
//
// $('#save_participants').on('click', function () {
// let employees_ids = []
// let employees_selected = {}
//
//     $('#tbody_modal_participants').find('.participant_item_selected').each(function () {
//         let id = $(this).attr('id').split('_')[2]
//         employees_ids.push(id)
//         employees_selected[id] = {
//             'name': $(this).find('.employee-name').text(),
//             'id': id,
//             'email': $(this).find('.employee-email').text()
//         }
//     })
//     if(employees_ids.length === 0){
//         toastr.error('Выберите участников')
//     }else {
//         let data = {
//             'employees_ids': employees_ids,
//             'study_id': study_id
//         }
//         btn_spinner($('#save_participants'))
//         $.ajax({
//             headers: { "X-CSRFToken": token },
//             url: url_save_study_participants,
//             type: 'POST',
//
//             data: JSON.stringify({
//                             'data': data
//                         }),
//             processData: false,
//             contentType: false,
//             error: function(data){
//                 toastr.error('Ошибка', data)
//             },
//             success:function (data) {
//                 $('.team-table').DataTable().clear().destroy()
//                 let data_json = data['response']
//                 let html = ''
//                 console.log(data_json)
//                 $.each(data_json, function (key, val) {
//                     let employee_invitation = val['invitation']
//                     let employee_email = val['email']
//                     let employee_name = val['name']
//                     let id = val['id']
//
//                     let employee_invitation_sent_datetime = val['invitation_sent_datetime']
//                     let completed_at_datetime = val['completed_at_datetime']
//                     let reminder = val['reminder']
//                     let questions_groups_arr = val['questions_groups_arr']
//                     let current_percentage = val['current_percentage']
//                     let total_questions_qnt = val['total_questions_qnt']
//                     let answered_questions_qnt = val['answered_questions_qnt']
//                     let filename = val['filename']
//                     html += '<tr class="" id="participant_id_' + id + '">'
//                     html += '<td>'
//                     if(answered_questions_qnt > 0){
//
//                         if(completed_at_datetime){
//                             html += '<i class="fa fa-circle font-color-success" aria-hidden="true" title="Опросник заполнен"><span style="color: transparent">3</span></i>'
//                         }else {
//                             html += '<i class="fa fa-circle font-color-warning" aria-hidden="true" title="Приглашение отправлено"><span style="color: transparent">2</span></i>'
//                         }
//                         html += '<span title="' + current_percentage + '%">'
//                         html += '<svg class="radial-progress" data-percentage="' + current_percentage + '" viewBox="0 0 80 80">'
//                         html += '<circle class="incomplete" cx="40" cy="40" r="35"></circle>'
//                         html += '<circle class="complete" cx="40" cy="40" r="35" style="stroke-dashoffset: 39.58406743523136;"></circle>'
//                         html += '</svg>'
//                         html += '</span>'
//
//                     }else {
//                         html += '<i class="fa fa-circle font-color-danger" aria-hidden="true" title="Приглашение не отправлено"><span style="color: transparent">1</span></i>'
//                     }
//                     html += '</td>'
//                     html += '<td>' + answered_questions_qnt + '/' + total_questions_qnt + '</td>'
//                     html += '<td>' + employee_name + '</td>'
//                     html += '<td>' + employee_email + '</td>'
//
//                     html += '<td class="participant_selected_questions_groups_td">'
//                     for(let i = 0; i < questions_groups_arr.length; i++){
//                         html += '<p class="mb-0 participant-selected-question-group" id="participant_selected_question_group_id_' + questions_groups_arr[i]['code'] +
//                             '">' + questions_groups_arr[i]['name'] + '</p>'
//                     }
//                     html += '</td>'
//
//                     html += '<td>' + employee_invitation_sent_datetime + '</td>'
//                     if(reminder !== ''){
//                         html += '<td>'
//                         for(let i=0; i < reminder.length; i++){
//                             html += reminder[i] + '<br>'
//                         }
//                         html += '</td>'
//                     }else {
//                         html += '<td></td>'
//                     }
//
//                     html += '<td>' +
//                         '<div style="text-align: center;" >' +
//                             '<i class="fe fe-more-vertical cursor-pointer" data-bs-toggle="dropdown" aria-expanded="false" style="font-size: 20px"></i>' +
//                             '<ul class="dropdown-menu">'
//                     if(employee_invitation){
//                         if(completed_at_datetime){
//                             html += '<li><a class="dropdown-item" href="/panel/download_single_report/' + filename + '">Скачать</a></li>'
//                         }else {
//                             html += '<li><a class="dropdown-item send-email-invitation cursor-pointer">Повторно отправить приглашение</a></li>'
//                         }
//                     }else {
//                         html += '<li><a class="dropdown-item send-email-invitation cursor-pointer">Отправить приглашение</a></li>'
//                         html += '<li> <a class = "dropdown-item add-question-groups cursor-pointer">Добавить группы вопросов</a></li>'
//                     }
//                     html += '</ul>' +
//                         '</div>' +
//                         '</td>'
//                     html += '</tr>'
//
//                 })
//                 $('#tbody_participants_selected').html(html)
//                 process_circle_progress()
//                 $('#modal_participants').modal('hide')
//                 btn_text($('#save_participants'), 'Сохранить')
//                 toastr.success('Участники обновлены')
//                 process_table_clear('.team-table')
//                 // $('.team-table').DataTable().raw(html).add()
//
//             }
//         });
//
//
//
//     }
//
//
// })
//
// $('#modal_send_invitation_btn').on('click', function () {
//     btn_spinner('#modal_send_invitation_btn')
//     let participant_tr_id = $('#modal_participant_name').attr('data-tr-id')
//     let participant_tr = $('#' + participant_tr_id)
//     let participant_id = participant_tr_id.split('_')[2]
//     let send_admin_notification_after_filling_up = 0
//     if ($('#send_admin_notification_after_filling_up').attr('checked') === 'checked') {
//         send_admin_notification_after_filling_up = 1
//     }
//     $.ajax({
//         headers: { "X-CSRFToken": token },
//         url: url_send_invitation_email,
//         type: 'POST',
//
//         data: JSON.stringify({
//                             'study_id': study_id,
//                             'participant_id': participant_id,
//                             'type': 'initial',
//                             'send_admin_notification_after_filling_up': send_admin_notification_after_filling_up
//                         }),
//         processData: false,
//         contentType: false,
//         error: function(data){
//             toastr.error('Ошибка', data)
//         },
//         success:function (data) {
//             let json_data = data['response']
//             if('error' in json_data){
//                 toastr.error(json_data['error'])
//             }else {
//                 if('company_error' in json_data){
//                     if(json_data['company_error'] === 'company_deactivated'){
//                         let output_html = '<hr class="solid mt-0" style="background-color: black;">' +
//                                         '<div>Компания деактивирована' + '</div>' +
//                                         '<div>Если Вы не знаете причин - обратитесь к менеджеру' + '</div>' +
//                                         '<br>' +
//                                         '<hr class="solid mt-0" style="background-color: black;">'
//                         Swal.fire({
//                           html: output_html,
//                           icon: 'warning',
//                           confirmButtonColor: '#3085d6',
//                           cancelButtonColor: '#d33',
//                           confirmButtonText: 'ОК'
//                         })
//                     }
//                 }else {
//                     let datetime_invitation_sent = json_data['datetime_invitation_sent'];
//                     let el = $('#participant_id_' + participant_id)
//                     el.find('.font-color-danger').removeClass('font-color-danger').addClass('font-color-warning').prop('title', 'Приглашение отправлено')
//                     el.find('.send-email-invitation').text('Повторно отправить приглашение')
//                     el.find('td:nth-child(6)').text(datetime_invitation_sent)
//                     el.find('td:nth-child(2)').text('0/' + json_data['questions_count'])
//                     toastr.success('Приглашение участнику отправлено')
//                 }
//             }
//
//             btn_text('#modal_send_invitation_btn', 'Отправить')
//             $('#modal_before_send_invitation').modal('hide')
//
//
//         }
//     });
//
// })
//
//
// $('#tbody_participants_selected').on('click', '.send-email-invitation', function () {
//     let role_name = $('#cur_role_name').text()
//     if ($('#company_active').attr('checked') !== 'checked' && role_name !== 'Админ заказчика') {
//         toastr.warning('Обратите внимание - компания деактивирована!')
//     }
//
//     let question_groups_qnt = $(this).closest('tr').find('.participant_selected_questions_groups_td p').length
//     if(question_groups_qnt === 0){
//         toastr.error('Выберите группы вопросов для участника')
//     }else {
//         let participant_name = $(this).closest('tr').find('td').eq(2).text()
//         let participant_email = $(this).closest('tr').find('td').eq(3).text()
//         $('#modal_participant_name').html('<b>' + participant_name + '</b>').attr('data-tr-id', $(this).closest('tr').attr('id'))
//         $('#modal_participant_email').html('<b>' + participant_email + '</b>')
//         $('#modal_before_send_invitation').modal('show')
//     }
// })
//
// $('#send_admin_notification_after_filling_up').on('click', function () {
//     if ($(this).attr('checked') === 'checked'){
//         $(this).attr('checked', false)
//         // active = 0
//     }else {
//         $(this).attr('checked', 'checked')
//         // active = 1
//     }
// })
//
//

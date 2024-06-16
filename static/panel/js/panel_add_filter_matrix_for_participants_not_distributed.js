expand_menu_item('#menu_matrix_filters_list')

$('#add_filter_position').on('click', function () {
    $('#tbody_filter_positions').append('<tr> \
            <td>\
            <select class="form-control form-select select_position" data-placeholder="Выберите должность"> \
                <option label="--Выберите должность--"></option> \
            </select> \
            </td> \
            <td style="text-align: center; vertical-align: middle;">\
                <div style="float: right">\
                    <i class="fe fe-x delete-position-row" style="font-size: 20px; cursor: pointer"></i>\
                </div>\
            </td>\
                    \
            </tr>')

    // categories.forEach(function (category) {
    //
    // })
    let last_tr = $('#tbody_filter_positions tr:last')
    let select_position = last_tr.find('.select_position').eq(0)
    positions.forEach(function (position) {
        select_position.append(`<option value="${position['id']}">${position['id']}. ${position['name']}</option>`)

    })
})

$('#tbody_filter_positions').on('click', '.delete-position-row', function () {
    $(this).closest('tr').remove()
})

$('#save_matrix_filter').on('click', function () {
    let square_ok = true
    let points_val_ok = true
    let points_comparison_ok = true
    let square = {}

    let positions_arr = []
    let positions_ok = true

    // console.log(`--- start ---`)
    // console.log(`categories_ok - ${categories_ok} categories_added - ${categories_added} categories_repeat_ok - ${categories_repeat_ok} points_val_ok - ${points_val_ok} points_comparison_ok - ${points_comparison_ok}`)
    // console.log(`------`)

    let square_val = $('#select_square option:selected').val()
    let square_name = $('#select_square option:selected').text()
    if(square_val === ''){
        square_ok = false
        toastr.error('Квадрат не выбран')
    }else {
        square['code'] =square_val
        square['name'] =square_name
    }

    $('#tbody_filter_positions tr').each(function (row) {
        let position_val = $(this).find('option:selected')
        if(position_val.val() === ''){
            $(this).remove()
        }else {
            if(jQuery.inArray(position_val.val(),positions_arr) === -1){
                positions_arr.push(position_val.val())
            }else {
                $(this).find('.select_position').css('background-color', 'red').css('color', 'white')
                positions_ok = false

            }
        }
    })

    if(!positions_ok){
        toastr.error('Есть повторяющиеся должности')
    }
    if(positions_arr.length === 0){
        toastr.error('Должности не добавлены')
    }
    // console.log(`positions_ok - ${positions_ok} categories_ok - ${categories_ok} square_ok - ${square_ok}`)
    // console.log(categories_arr)
    // console.log(positions_arr)

    if(positions_ok && square_ok && positions_arr.length !== 0){
        // console.log('save')
        btn_spinner('#save_matrix_filter')
        $.ajax({
            headers: {"X-CSRFToken": token},
            url: url_save_new_matrix_filter_for_participants_not_distributed,
            type: 'POST',
            data: JSON.stringify({
                'positions': positions_arr,
                'square': square,
            }),
            processData: false,
            contentType: false,
            error: function (data) {
                toastr.error('Ошибка', data)
            },
            success: function (data) {
                console.log(data)
                btn_text('#save_matrix_filter', 'Сохранить фильтр')
                let output_html = '<h2 class="mb-0" style="text-align: center">Данные сохранены</h2>' +
                                    '<br>' +
                                    '<hr class="solid mt-0" style="background-color: black;">' +
                                    '<h4 style="text-align: center">Фильтр добавлен</h4>' +
                                    '<hr class="solid mt-0" style="background-color: black;">'

                Swal.fire({
                    html: output_html,
                    icon: 'success',
                    confirmButtonColor: '#3085d6',
                    cancelButtonColor: '#d33',
                    confirmButtonText: 'ОК'
                }).then((result) => {
                    if (result.value) {
                        window.location.href = url_filters_matrix_list
                    }
                })

            }
        })


    }
})

$('#tbody_filter_categories').on('click', '.points_from', function () {
    $(this).css('background-color', 'white').css('color', '#76839a')
})

$('#tbody_filter_categories').on('click', '.points_to', function () {
    $(this).css('background-color', 'white').css('color', '#76839a')
})

$('#tbody_filter_categories').on('click', '.select_category', function () {
    $(this).css('background-color', 'white').css('color', '#76839a')
})

$('#tbody_filter_positions').on('click', '.select_position', function () {
    $(this).css('background-color', 'white').css('color', '#76839a')
})








// squares_data.forEach(function (square) {
//     $('#select_square').append(
//         `<option value="${square['code']}">${square['square_name']} - ${square['square_role_name']}</option>`
//     )
//
// })



// process_table_clear('#table_participants_for_study')

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
// $('#add_filter_category').on('click', function () {
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



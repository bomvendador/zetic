expand_menu_item('#menu_companies_studies_list')

process_table_clear('#table_participants_for_study')

$('#select_company').on("select2:select", function(e) {
    let company_active = $('#select_company :selected').attr('data-company-active')
    if(company_active === 'True'){
        $('#company_active').prop('checked', 'checked')
    }else {
        $('#company_active').prop('checked', '')
    }
    $('#table_participants_for_study').DataTable().destroy()
    $('#tbody_participants_selected').html('')
     process_table_clear('#table_participants_for_study')
});

$('#save_study').on('click', function () {
    let employees_ids = []
    let company_id = $('#select_company :selected').attr('id').split('_')[2]
    let test_ok = true
    $('#tbody_participants_selected tr').each(function () {
        employees_ids.push($(this).attr('data-employee-id'))
    })
    if(employees_ids.length === 0 || $('#tbody_participants_selected tr .dataTables_empty').length === 1){
        test_ok = false
        toastr.error('Список участников исследования пуст')
    }
    let template_id = $('#select_template :selected').val()
    if(template_id === ''){
        test_ok = false
        toastr.error('Необходимо выбрать шаблон')

    }
    let input_study_name = $('#input_study_name').val()
    if(input_study_name === ''){
        test_ok = false
        toastr.error('Название должно быть заполнено')

    }

    if(test_ok){
        btn_spinner('#save_study')
        $.ajax({
            headers: {"X-CSRFToken": token},
            url: url_add_new_study,
            type: 'POST',
            data: JSON.stringify({
                'template_id': template_id,
                'employees_ids': employees_ids,
                'input_study_name': input_study_name,
                'company_id': company_id,
            }),
            processData: false,
            contentType: false,
            error: function (data) {
                toastr.error('Ошибка', data)
            },
            success: function (data) {
                btn_text('#save_study', 'Сохранить исследование')
                // hide_progressbar_loader()
                // let employees = data['response']['employees']
                Swal.fire({
                  title: 'Данные сохранены',
                  text: "Исследование добавлено",
                  icon: 'success',
                  confirmButtonColor: '#3085d6',
                  cancelButtonColor: '#d33',
                  confirmButtonText: 'ОК'
                }).then((result) => {
                    if (result.isConfirmed) {
                        window.location.href = url_studies_list
                    }
                })

            }
        })


    }



})


$('#add_participants').on('click', function () {
    let company_id = $('#select_company').val()
    let company_id_is_empty = false
    if(company_id === ''){
        company_id_is_empty = true
    }

    if(!company_id_is_empty){
        // $('#modal_add_participant')
        // $('#tbody_participants_to_choose').html('')
        show_progressbar_loader()
        $.ajax({
            headers: { "X-CSRFToken": token },
            url: url_get_company_employees_for_new_study,
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
                hide_progressbar_loader()
                let employees = data['response']['employees']
                // console.log(employees)
                // process_table('.team-table')
                let participants_already_added_ids = []
                $('#tbody_participants_selected tr').each(function () {
                    participants_already_added_ids.push($(this).attr('data-employee-id'))
                })
                console.log(participants_already_added_ids)
                $('#modal_add_participant').DataTable().destroy()
                $('#tbody_participants_to_choose').html('')
                employees.forEach(function (employee) {
                    console.log(employee)
                    console.log($.inArray(employee['id'], participants_already_added_ids))
                    if($.inArray(employee['id'].toString(), participants_already_added_ids) === -1){
                        let html = `<tr id="employee_id_${employee['id']}">` +
                            '         <td>\n' +
                            '            <input type="checkbox" class="" name="example-checkbox1" value="option1" style="transform: scale(1.1)">\n' +
                            `         </td>\n` +
                            `         <td>${employee['name']}</td>` +
                            `         <td>${employee['email']}</td>` +
                            `         <td>${employee['industry']}</td>` +
                            `         <td>${employee['role']}</td>` +
                            `         <td>${employee['position']}</td>` +
                            `         <td>${employee['birth_year']}</td>` +
                            `         <td>${employee['sex']}</td>` +
                            `        </tr>`
                        $('#tbody_participants_to_choose').append(html)

                    }
                })
                process_table_clear('#modal_add_participant')
            }
        });

        $('#check_all_employees_for_study').prop('checked', '')
        $('#modal_participants').modal('show')
    }else {
        Swal.fire({
          title: 'Данные отсутствуют',
          text: "Компания должна быть выбрана",
          icon: 'warning',
          confirmButtonColor: '#3085d6',
          cancelButtonColor: '#d33',
          confirmButtonText: 'ОК'
        })

    }
})

$('#check_all_employees_for_study').on('click', function () {
    console.log($(this).prop('checked'))
        if($(this).prop('checked') === true){
            $('#tbody_participants_to_choose input').each(function (index) {
                $(this).prop('checked', 'checked')
            })
        }else {
            $('#tbody_participants_to_choose input').each(function (index) {
                $(this).prop('checked', '')
            })

        }

})

$('#add_participants_to_study').on('click', function () {
    let html_for_study_list
    let row_html
    $('#tbody_participants_to_choose tr').each(function (index) {
        if($(this).find('input').prop('checked') === true){
            let id = $(this).attr('id').split('_')[2]
            let name = $(this).find('td').eq(1).text()
            let email = $(this).find('td').eq(2).text()
            let industry = $(this).find('td').eq(3).text()
            let role = $(this).find('td').eq(4).text()
            let position = $(this).find('td').eq(5).text()
            let birth_year = $(this).find('td').eq(6).text()
            let sex = $(this).find('td').eq(7).text()
            row_html = `<tr data-employee-id="${id}">` +
                        `<td>${name}</td>` +
                        `<td>${email}</td>` +
                        `<td>${industry}</td>` +
                        `<td>${role}</td>` +
                        `<td>${position}</td>` +
                        `<td>${birth_year}</td>` +
                        `<td>${sex}</td>` +
                        `<td><i class="fe fe-x remove-participant-from-study" style="font-size: 18px; cursor: pointer" title="Удалить"></i></td>` +
                        `</tr>`
            html_for_study_list = html_for_study_list + row_html
        }
    })
    $('#table_participants_for_study').DataTable().destroy()
    $('#tbody_participants_selected').append(html_for_study_list)
     process_table_clear('#table_participants_for_study')
    $('#modal_participants').modal('hide')
})

$('#tbody_participants_selected').on('click', '.remove-participant-from-study', function () {
    console.log('rrrrr')
    $('#table_participants_for_study').DataTable().destroy()
    $(this).closest('tr').remove()
    process_table_clear('#table_participants_for_study')

})



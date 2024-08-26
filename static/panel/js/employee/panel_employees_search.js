expand_menu_item('#menu_employee_search')

process_table_clear('#table_employees_search')

$('#start_employees_search').on('click', function () {
    let fio = $('#input_fio').val()
    let email = $('#input_email').val()
    if (fio === '' && email === '') {
        toastr.error('ФИО и/или Email должны быть заполнены')
    } else {
        btn_spinner('#start_employees_search')
        $.ajax({
            headers: {"X-CSRFToken": token},
            url: url_search_for_employees,
            type: 'POST',
            data: JSON.stringify({
                'fio': fio,
                'email': email,
            }),
            processData: false,
            contentType: false,
            error: function (data) {
                toastr.error('Ошибка', data)
            },
            success: function (data) {
                btn_text('#start_employees_search', 'Начать поиск')
                // hide_progressbar_loader()
                $('#table_employees_search').DataTable().destroy()
                $('#table_employees_search_tbody').html(data['rows'])
                process_table_clear('#table_employees_search')
            }
        });


    }
})

$('#select_company').on("select2:select", function (e) {
    console.log($(this).val())
    let company_id = $(this).val()

    show_progressbar_loader()
    $.ajax({
        headers: {"X-CSRFToken": token},
        url: url_search_for_employees,
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
            hide_progressbar_loader()
            // console.log(data)
            if (data === 'no_projects') {
                toastr.warning('Проекты для выбранной компании отсутствуют')
            } else {
                $('#table_projects').DataTable().destroy()
                $('#company_projects_tbody').html(data)

                process_table_clear('#table_projects')

            }
        }
    });

});


$('#add_project').on('click', function () {
    window.location.href = url_add_new_project
})

$('#add_participants').on('click', function () {
    let company_id = $('#select_company').val()
    let company_id_is_empty = false
    if (company_id === '') {
        company_id_is_empty = true
    }

    if (!company_id_is_empty) {
        // $('#modal_add_participant')
        // $('#tbody_participants_to_choose').html('')
        show_progressbar_loader()
        $.ajax({
            headers: {"X-CSRFToken": token},
            url: url_get_company_employees_for_new_study,
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
                hide_progressbar_loader()
                let employees = data['response']['employees']
                // console.log(employees)
                // process_table('.team-table')
                let participants_already_added_ids = []
                $('#tbody_participants_selected tr').each(function () {
                    participants_already_added_ids.push($(this).attr('data-employee-id'))
                })
                // console.log(participants_already_added_ids)
                $('#modal_add_participant').DataTable().destroy()
                $('#tbody_participants_to_choose').html('')
                employees.forEach(function (employee) {
                    // console.log(employee)
                    // console.log($.inArray(employee['id'], participants_already_added_ids))
                    if ($.inArray(employee['id'].toString(), participants_already_added_ids) === -1) {
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
    } else {
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
    if ($(this).prop('checked') === true) {
        $('#tbody_participants_to_choose input').each(function (index) {
            $(this).prop('checked', 'checked')
        })
    } else {
        $('#tbody_participants_to_choose input').each(function (index) {
            $(this).prop('checked', '')
        })

    }

})

$('#add_participants_to_study').on('click', function () {
    let html_for_study_list
    let row_html
    $('#tbody_participants_to_choose tr').each(function (index) {
        if ($(this).find('input').prop('checked') === true) {
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




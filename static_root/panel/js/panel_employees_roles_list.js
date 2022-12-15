expand_menu_item('#menu_employees_roles_list')

$('#add_role').on('click', function () {
    $('#input_modal_add_role').modal('show')
})

$('#save_new_role').on('click', function () {
    let name_ru = $('#input_role_ru_name').val()
    let name_en = $('#input_role_en_name').val()

    let dict = {
        'name_ru': name_ru,
        'name_en': name_en
    }

    if(name_ru === '' && name_en === ''){
        toastr.error('Хотя бы одно поле должно быть заполнено')
    }else {
        btn_spinner($('#save_new_role'))
        save_company_parameter(dict, url_save_new_employee_role, '#input_modal_add_role', 'Роль добавлена', 'Роль сотрудника успешно добавлена')
    }
})

let role_id

$('.edit-role').on('click', function () {
    role_id = $(this).closest('ul').attr('id').split("_")[2]
    let name_ru = $(this).closest('tr').find('.role-name-ru').text().trim()
    let name_en = $(this).closest('tr').find('.role-name-en').text().trim()
    $('#input_role_ru_edit_name').val(name_ru)
    $('#input_role_en_edit_name').val(name_en)

    $('#input_modal_edit_role').modal('show')

})

$('#edit_role').on('click', function () {
    let name_ru = $('#input_role_ru_edit_name').val()
    let name_en = $('#input_role_en_edit_name').val()

    if(name_ru === '' && name_en === ''){
        toastr.error('Хотя бы одно поле должно быть заполнено')
    }else {
        let dict = {
            'name_ru': name_ru,
            'name_en': name_en,
            'id': role_id
        }
        btn_spinner($('#edit_role'))
        save_company_parameter(dict, url_edit_employee_role, '#input_modal_edit_role','Данные обновлены', 'Данные роли сотрудника успешно обновлены')
    }
})

$('.delete-role').on('click', function () {
    Swal.fire({
        title: 'Удаление роли',
        text: "Удалить роль сотрудника?",
        icon: 'question',
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Да',
        cancelButtonText: 'Нет',
        showCancelButton: true
    }).then((result) => {
        if (result.isConfirmed) {
            role_id = $(this).closest('ul').attr('id').split("_")[2]
            let dict = {
                'id': role_id
            }
            save_company_parameter(dict, url_delete_employee_role, '', '', '')
        }
    })

})

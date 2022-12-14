expand_menu_item('#menu_employees_positions_list')

$('#add_position').on('click', function () {
    $('#input_modal_add_position').modal('show')
})

$('#save_new_position').on('click', function () {
    let name_ru = $('#input_position_ru_name').val()
    let name_en = $('#input_position_en_name').val()

    let dict = {
        'name_ru': name_ru,
        'name_en': name_en
    }

    if(name_ru === '' && name_en === ''){
        toastr.error('Хотя бы одно поле должно быть заполнено')
    }else {
        btn_spinner($('#save_new_position'))
        save_company_parameter(dict, url_save_new_employee_position, '#input_modal_add_position', 'Должность добавлена', 'Должность сотрудника успешно добавлена')
    }
})

let id

$('.edit-position').on('click', function () {
    id = $(this).closest('ul').attr('id').split("_")[2]
    let name_ru = $(this).closest('tr').find('.name-ru').text().trim()
    let name_en = $(this).closest('tr').find('.name-en').text().trim()
    $('#input_position_ru_edit_name').val(name_ru)
    $('#input_position_en_edit_name').val(name_en)

    $('#input_modal_edit_position').modal('show')

})

$('#edit_position').on('click', function () {
    let name_ru = $('#input_position_ru_edit_name').val()
    let name_en = $('#input_position_en_edit_name').val()

    if(name_ru === '' && name_en === ''){
        toastr.error('Хотя бы одно поле должно быть заполнено')
    }else {
        let dict = {
            'name_ru': name_ru,
            'name_en': name_en,
            'id': id
        }
        btn_spinner($('#edit_position'))
        save_company_parameter(dict, url_edit_employee_position, '#input_modal_edit_position','Данные обновлены', 'Данные должности сотрудника успешно обновлены')
    }
})

$('.delete-position').on('click', function () {
    Swal.fire({
        title: 'Удаление должности',
        text: "Удалить должность сотрудника?",
        icon: 'question',
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Да',
        cancelButtonText: 'Нет',
        showCancelButton: true
    }).then((result) => {
        if (result.isConfirmed) {
            id = $(this).closest('ul').attr('id').split("_")[2]
            let dict = {
                'id': id
            }
            save_company_parameter(dict, url_delete_employee_position, '', '', '')
        }
    })

})

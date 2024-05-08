expand_menu_item('#menu_industries_list')

$('#add_industry').on('click', function () {
    $('#input_modal_add_industry').modal('show')
})

$('#save_new_industry').on('click', function () {
    let name_ru = $('#input_industry_ru_name').val()
    let name_en = $('#input_industry_en_name').val()

    let dict = {
        'name_ru': name_ru,
        'name_en': name_en
    }

    if(name_ru === '' && name_en === ''){
        toastr.error('Хотя бы одно поле должно быть заполнено')
    }else {
        btn_spinner($('#save_new_industry'))
        save_company_parameter(dict, url_save_new_industry, '#input_modal_add_industry', 'Индустрия добавлена', 'Индустрия успешно добавлена')
    }
})

let industry_id

$('.edit-industry').on('click', function () {
    industry_id = $(this).closest('ul').attr('id').split("_")[2]
    let name_ru = $(this).closest('tr').find('.industry-name-ru').text().trim()
    let name_en = $(this).closest('tr').find('.industry-name-en').text().trim()
    $('#input_industry_ru_edit_name').val(name_ru)
    $('#input_industry_en_edit_name').val(name_en)

    $('#input_modal_edit_industry').modal('show')

})

$('.delete-industry').on('click', function () {


    Swal.fire({
        title: 'Удаление индустрии',
        text: "Удалить индустрию?",
        icon: 'question',
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Да',
        cancelButtonText: 'Нет',
        showCancelButton: true
    }).then((result) => {
        if (result.value) {
            industry_id = $(this).closest('ul').attr('id').split("_")[2]
            let dict = {
                'id': industry_id
            }
            save_company_parameter(dict, url_delete_industry, '', 'Запись удалена', 'Индустрия успешно удалена')
        }
    })

})


$('#edit_industry').on('click', function () {
    let name_ru = $('#input_industry_ru_edit_name').val()
    let name_en = $('#input_industry_en_edit_name').val()

    if(name_ru === '' && name_en === ''){
        toastr.error('Хотя бы одно поле должно быть заполнено')
    }else {
        let dict = {
            'name_ru': name_ru,
            'name_en': name_en,
            'id': industry_id
        }

        btn_spinner($('#edit_industry'))
        save_company_parameter(dict, url_edit_industry, '#input_modal_edit_industry','Данные обновлены', 'Данные индустрии успешно обновлены')

    }
})



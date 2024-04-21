expand_menu_item('#menu_categories_list')

let category_id
let categories_table
let first_show = true
let section_name
let section_id

$('#section_select').on('change', function () {
    let option_text = $(this).find(':selected').val()
    if (option_text !== '-- Выберите секцию --') {
        first_show = false
        section_id = $(this).find(':selected').attr('id').split('_')[2]
        section_name = $(this).find(':selected').val()
        console.log(section_id)
        show_progressbar_loader()
        $.ajax({
            headers: {"X-CSRFToken": token},
            url: url_get_categories_by_section,
            type: 'POST',
            data: JSON.stringify({
                'section_id': section_id
            }),
            processData: false,
            contentType: false,
            error: function (data) {
                toastr.error('Ошибка', data)
            },
            success: function (data) {
                console.log(data['response'])
                // jQuery.each(data, function () {
                //
                // })
                // let categories_table = process_table_clear('#categories_table')
                $('#categories_table').fadeOut(500, function () {
                    let html = ''

                    $('#categories_tbody').html('')
                    data['response'].forEach(function (el) {
                        // categories_table.row.add(el)
                        html = '<tr id="category_id_' + el['id'] + '" data-code="' + el['code'] + '">' +
                            '<td class="category-name-ru">' + el['name'] + '</td>' +
                            '<td class="">' + el['section'] + '</td>' +
                            '<td class="">' + el['code'] + '</td>' +
                            '<td class="">' + el['created_at'] + '</td>' +
                            '<td class="">' + el['created_by'] + '</td>' +
                            '<td>' +
                            '<div style="text-align: center;">\n' +
                            '    <i class="fe fe-more-vertical cursor-pointer" data-bs-toggle="dropdown" aria-expanded="false" style="font-size: 20px"></i>\n' +
                            '    <ul class="dropdown-menu" id="category_id_' + el['id'] + '">\n' +
                            '        <li>\n' +
                            '            <a class="dropdown-item edit-category cursor-pointer">\n' +
                            '                <svg style="margin-right: 5px" xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-edit-2"><path d="M17 3a2.828 2.828 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5L17 3z"></path></svg>\n' +
                            '                Изменить\n' +
                            '            </a>\n' +
                            '        </li>\n' +
                            '        <li>\n' +
                            '            <a class="dropdown-item cursor-pointer" href="questions/'+ el['id'] + '">\n' +
                            '            <svg style="margin-right: 5px"  width="15" height="15" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">\n' +
                            '<path d="M10.125 8.875C10.125 7.83947 10.9645 7 12 7C13.0355 7 13.875 7.83947 13.875 8.875C13.875 9.56245 13.505 10.1635 12.9534 10.4899C12.478 10.7711 12 11.1977 12 11.75V13" stroke="#1C274C" stroke-width="1.5" stroke-linecap="round"/>\n' +
                            '<circle cx="12" cy="16" r="1" fill="#1C274C"/>\n' +
                            '<path d="M7 3.33782C8.47087 2.48697 10.1786 2 12 2C17.5228 2 22 6.47715 22 12C22 17.5228 17.5228 22 12 22C6.47715 22 2 17.5228 2 12C2 10.1786 2.48697 8.47087 3.33782 7" stroke="#1C274C" stroke-width="1.5" stroke-linecap="round"/>\n' +
                            '</svg>\n' +
                            '            Вопросы\n' +
                            '            </a>\n' +
                            '        </li>\n' +
                            '        <li>\n' +
                            '            <a class="dropdown-item delete-category cursor-pointer font-color-danger">\n' +
                            '            <svg style="margin-right: 5px" xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-trash-2"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path><line x1="10" y1="11" x2="10" y2="17"></line><line x1="14" y1="11" x2="14" y2="17"></line></svg>\n' +
                            '            Удалить\n' +
                            '            </a>\n' +
                            '        </li>\n' +
                            '    </ul>\n' +
                            '</div>\n' +
                            '</td>' +
                            '</tr>'
                        $('#categories_tbody').append(html)

                        // console.log(el['name'])
                    })
                    let html_table = $('#categories_table').html()
                    $('#categories_table').DataTable().clear().destroy()
                    $('#categories_table').html(html_table)
                    process_table('#categories_table')

                    $('#categories_table').fadeIn(500)
                    hide_progressbar_loader()
                    $('#add_category').fadeIn(500)

                })

                // categories_table.draw()
            }
        });


    }else {
        if(!first_show){
            // $('#categories_table').fadeOut(100)
            // $('#categories_tbody').html('')

            $('#categories_table').DataTable().clear().destroy()


            process_table($('#categories_table'))
            $('#categories_table').fadeIn(500)
            // $('#categories_table').DataTable().clear()
            $('#add_category').fadeOut(500)

        }
    }

})

$('#add_category').on('click', function () {
    $('#modal_section_name').text(section_name)
    $('#input_modal_add_category').modal('show')
})

// $('#main-container').on('click', '#add_category', function () {
//     $('#input_modal_add_category').modal('show')
//     console.log('fgfgdgdfdfgd')
// })

$('#save_new_category').on('click', function () {
    let name = $('#input_category_name').val()
    let code = $('#input_category_code').val()
    if (name === '' || code === []) {
        toastr.error('Название и код должны быть заполнены')
    } else {
        btn_spinner($('#save_new_category'))
        $.ajax({
            headers: {"X-CSRFToken": token},
            url: url_save_new_category,
            type: 'POST',
            data: JSON.stringify({
                'name': name,
                'code': code,
                'section_id': section_id
            }),
            processData: false,
            contentType: false,
            error: function (data) {
                toastr.error('Ошибка', data)
            },
            success: function (data) {
                console.log(data)
                $('#input_modal_add_category').modal('hide')
                Swal.fire({
                    title: 'Категория добавлена',
                    text: "Данные успешено обновлены",
                    icon: 'success',
                    confirmButtonColor: '#3085d6',
                    cancelButtonColor: '#d33',
                    confirmButtonText: 'ОК'
                }).then((isConfirmed) => {
                    if (isConfirmed) {
                        $("#section_select #section_id_" + section_id).change();
                        btn_text($('#save_new_category'), 'Сохранить')
                        $('#input_category_name').val('')
                        $('#input_category_code').val('')
                        // window.location.reload()
                    }
                })
            }
        });
    }
})


$('#categories_table').on('click', '.edit-category', function () {
    category_id = $(this).closest('ul').attr('id').split("_")[2]
    console.log(`category_id = ${category_id}`)
    let name = $(this).closest('tr').find('.category-name-ru').text().trim()
    let code = $(this).closest('tr').attr('data-code')
    $('#input_category_edit_name').val(name)
    $('#input_category_edit_code').val(code)

    $('#input_modal_edit_category').modal('show')

})

$('#main-container').on('click', '.delete-category', function () {
    Swal.fire({
        title: 'Удаление категории',
        text: "Удалить категории?",
        icon: 'question',
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Да',
        cancelButtonText: 'Нет',
        showCancelButton: true
    }).then((result) => {
        if (result.value) {
            category_id = $(this).closest('ul').attr('id').split("_")[2]
            $.ajax({
                headers: {"X-CSRFToken": token},
                url: url_delete_category,
                type: 'POST',
                data: JSON.stringify({
                    'category_id': category_id
                }),
                processData: false,
                contentType: false,
                error: function (data) {
                    toastr.error('Ошибка', data)
                },
                success: function (data) {
                    console.log(data)
                    if(data['error']){
                        Swal.fire({
                            title: 'Ошибка',
                            text: data['error'],
                            icon: 'error',
                            confirmButtonColor: '#3085d6',
                            cancelButtonColor: '#d33',
                            confirmButtonText: 'ОК'
                        })
                    }else {
                        Swal.fire({
                            title: 'Категория удалена',
                            text: "Данные успешено обновлены",
                            icon: 'success',
                            confirmButtonColor: '#3085d6',
                            cancelButtonColor: '#d33',
                            confirmButtonText: 'ОК'
                        }).then((isConfirmed) => {
                            if (isConfirmed) {

                                $("#section_select #section_id_" + section_id).change();
                            }
                        })

                    }
                }
            });
        }
    })

})


$('#edit_category').on('click', function () {
    let name = $('#input_category_edit_name').val()
    let code = $('#input_category_edit_code').val()

    if (name === '' || code === '') {
        toastr.error('Название и код должны быть заполнено')
    } else {

        btn_spinner($('#edit_category'))
        $.ajax({
            headers: {"X-CSRFToken": token},
            url: url_edit_category,
            type: 'POST',
            data: JSON.stringify({
                'name': name,
                'code': code,
                'category_id': category_id
            }),
            processData: false,
            contentType: false,
            error: function (data) {
                toastr.error('Ошибка', data)
            },
            success: function (data) {
                console.log(data)
                $('#categories_tbody').find(`#category_id_${data['category_id']}`).attr('data-code', data['code'])
                $('#categories_tbody').find(`#category_id_${data['category_id']}`).find('.category-name-ru').eq(0).text(data['name'])
                // $('#input_category_edit_name').val(data['name'])
                // $('#input_category_code').val(data['code'])
                $('#input_modal_edit_category').modal('hide')
                Swal.fire({
                    title: 'Категория обновлена',
                    text: "Данные успешено обновлены",
                    icon: 'success',
                    confirmButtonColor: '#3085d6',
                    cancelButtonColor: '#d33',
                    confirmButtonText: 'ОК'
                }).then((isConfirmed) => {
                    if (isConfirmed) {
                        $(`#category_id_${data['category_id']} td`).eq(0).text(data['name'])
                        btn_text('#edit_category', 'Сохранить')
                        // window.location.reload()
                    }
                })
            }
        });


    }
})



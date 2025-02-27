// expand_menu_item('#menu_individual_report_points_description_filters_list')

let current_group_id
let group_parent_node = $('#potential_matrix_conditions_body')

if (groups_by_levels !== '') {
    $(document).ready(function () {
        let level_cnt = 0
        groups_by_levels.forEach(function (level) {
            level[level_cnt].forEach(function (level_group) {
                add_existing_group(level_group)
            })
            level_cnt++
        })

    })
}
group_parent_node.on('click', '.add-item', function () {
    current_group_id = $(this).closest('.condition-group').attr('id')
    let panel_body = $(this).closest('.panel').find('.panel-body')
    let groups_cnt = panel_body.find('.condition-group').length
    let categories_tables_cnt = panel_body.find('.categories-table').length
    $('#select_item').html('<option value="0">-- Сделайте выбор --</option>')
    if (groups_cnt > 0) {
        $('#select_item').append('<option value="group">Группа</option>')
    }
    if (categories_tables_cnt > 0) {
        $('#select_item').append('<option value="category">Категория</option>')
    }
    if (categories_tables_cnt === 0 && groups_cnt === 0) {
        $('#select_item').append('<option value="group">Группа</option>').append('<option value="category">Категория</option>')
    }

    $('#modal_add_item').modal('show')
})


$('#modal_add_item_btn').on('click', function () {
    let selected_option = $('#select_item').val()
    let current_group_node = $('#' + current_group_id)
    let current_group_panel_body = current_group_node.find('.panel-body').eq(0)

    switch (selected_option) {
        case '0':
            toastr.error('Выберите элемент добавления')
            break;
        case 'group':
            $('#modal_add_item').modal('hide')
            add_group(group_parent_node, current_group_node, current_group_panel_body, '')
            console.log(selected_option)
            break;
        case 'category':
            $('#modal_add_item').modal('hide')
            console.log(selected_option)
            let categories_table_node = current_group_node.find('.categories-table')
            let tables_cnt = categories_table_node.length
            let category_tr = $('#category_tr_template').html()

            if (tables_cnt === 0) {
                let table_html = $('#potential_matrix_category_table_template').html()
                current_group_panel_body.html(table_html)
                categories_table_node = current_group_node.find('.categories-table').eq(0)
                categories_table_node.data('table-group-id', current_group_id)
                console.log(`categories_table_node = ${categories_table_node.data('table-group-id')}`)

                current_group_panel_body.find('.categories-table-tbody').eq(0).html(category_tr)
            } else {
                current_group_panel_body.find('.categories-table-tbody').eq(0).append(category_tr)
            }
            current_group_node.find('#' + current_group_id + '_content').last().addClass('show') //открыть родительскую группу

            break;
        default:
            break;
    }
})

$('#add_filter_category').on('click', function () {
    let html = $('#category_tr_template').html()
    $('#tbody_filter_categories').append(html)

})

$('#potential_matrix_conditions_body').on('click', '.delete-category-row', function () {
    if ($(this).closest('tbody').find('tr').length === 1) {
        console.log($(this).closest('tbody').find('tr').length)
        $(this).closest('.categories-table').remove()
    }
    $(this).closest('tr').remove()

})



$('#description_card_body').on('click', 'textarea', function () {
    $(this).removeClass('is-invalid state-invalid')
})

function check_groups(group_parent_node) {
    let local_groups_ok = true
    group_parent_node.find('.group-content-body').each(function () {
        if ($(this).html().trim() === '') {
            local_groups_ok = false
        }
    })
    return local_groups_ok
}

$('#save_potential_matrix').on('click', function () {
    let categories_ok = true
    let categories_added = true
    let categories_repeat_ok = true
    let square_ok = true
    let points_val_ok = true
    let points_comparison_ok = true
    let groups_ok = true
    let categories_val_arr = []
    let categories_arr = []
    let square = $('#square').val()
    console.log(square)
    if (square === '' || square === '0') {
        toastr.error('Выберите квадрат')
        square_ok = false
    }
    group_parent_node.find('.categories-table-tbody tr').each(function (row) {
        // $('#tbody_filter_categories tr').each(function (row) {

        let category_val = $(this).find('.select_category option:selected').val()
        if (category_val === '') {
            let closest_categories_table_node = $(this).closest('.categories-table')
            $(this).remove()
            if (closest_categories_table_node.find('.categories-table-tbody tr').length === 0) {
                closest_categories_table_node.remove()
                groups_ok = check_groups(group_parent_node)
            }
            // } else if (jQuery.inArray(category_val, categories_val_arr) === -1) {
        } else {
            // the element is not in the array
            let points_from = $(this).find('.points_from').eq(0)
            let points_to = $(this).find('.points_to').eq(0)
            categories_val_arr.push(category_val)
            if (points_from.val() === '') {
                points_val_ok = false
                points_from.css('background-color', 'red').css('color', 'white')
            }
            if (points_to.val() === '') {
                points_val_ok = false
                points_to.css('background-color', 'red').css('color', 'white')
            }

            if (points_val_ok) {
                if (Number(points_from.val()) >= Number(points_to.val())) {
                    points_comparison_ok = false
                    points_from.css('background-color', 'red').css('color', 'white')
                    points_to.css('background-color', 'red').css('color', 'white')
                }
            }

            if (!points_comparison_ok || !points_val_ok) {
                categories_ok = false
            }
        }

    })
    // if (group_parent_node.find('.categories-table-tbody .tr').length === 0) {
    if (group_parent_node.find('.categories-table-tbody tr').length === 0) {
        categories_added = false
        toastr.error('Шкалы не добавлены')
    }
    if (!check_groups(group_parent_node)) {
        toastr.error('Группы не могут быть пустыми')
        groups_ok = check_groups(group_parent_node)
    }


    if (!categories_repeat_ok) {
        toastr.error('Есть повторяющиеся шкалы')
    }

    if (!points_val_ok) {
        toastr.error('Есть пустые баллы')
    }
    if (!points_comparison_ok) {
        toastr.error('Баллы ОТ должны быть меньше Баллов ДО')
    }

    if (categories_ok && square_ok && categories_added && groups_ok) {
        // console.log('save')
        let groups_data = []
        group_parent_node.find('.condition-group').each(function () {
            let group_id = $(this).attr('id')
            let parent_group_id = $(this).data('parent-group-id')
            let level = $(this).data('level')
            let group_type = $(this).find('.group-type').eq(0).val()
            let group_categories_arr = []

            let group_categories = $(this).find('.categories-table')
            group_categories.each(function () {
                if ($(this).data('table-group-id') === group_id) {
                    group_categories.eq(0).find('.categories-table-tbody tr').each(function () {
                        let category_value = $(this).find('.select_category option:selected').val()
                        let points_from_value = $(this).find('.points_from').eq(0).val()
                        let points_to_value = $(this).find('.points_to').eq(0).val()
                        group_categories_arr.push({
                            'category_id': category_value,
                            'points_from': points_from_value,
                            'points_to': points_to_value,
                        })
                    })

                }
            })
            groups_data.push({
                'group_id': group_id,
                'parent_group_id': parent_group_id,
                'group_type': group_type,
                'group_categories_arr': group_categories_arr,
                'level': level
            })
        })
        console.log(groups_data)
        // return
        btn_spinner('#save_potential_matrix')
        $.ajax({
            headers: {"X-CSRFToken": token},
            url: url_save_potential_matrix,
            type: 'POST',
            data: JSON.stringify({
                'groups_data': groups_data,
                'square_code': square,
                'matrix_id': matrix_id,
                'project_id': project_id,
            }),
            processData: false,
            contentType: false,
            error: function (data) {
                toastr.error('Ошибка', data)
            },
            success: function (data) {
                // console.log(data)
                btn_text('#save_potential_matrix', 'Сохранить матрицу')
                let name_type = ''
                if (matrix_id === '') {
                    name_type = 'создана'
                } else {
                    name_type = 'обновлена'
                }
                let output_html = '<h2 class="mb-0" style="text-align: center">Данные сохранены</h2>' +
                    '<br>' +
                    '<hr class="solid mt-0" style="background-color: black;">' +
                    '<h4 style="text-align: center">Матрица ' + name_type + '</h4>' +
                    '<hr class="solid mt-0" style="background-color: black;">'

                Swal.fire({
                    html: output_html,
                    icon: 'success',
                    confirmButtonColor: '#3085d6',
                    cancelButtonColor: '#d33',
                    confirmButtonText: 'ОК'
                }).then((result) => {
                    if (result.value) {
                        if (url_edit_project === '') {
                            window.location.href = url_potential_matrix_list

                        } else {
                            window.location.href = url_edit_project

                        }
                    }
                })

            }
        })


    }
})

group_parent_node.on('click', '.points_from', function () {
    $(this).css('background-color', 'white').css('color', '#76839a')
})

group_parent_node.on('click', '.points_to', function () {
    $(this).css('background-color', 'white').css('color', '#76839a')
})

group_parent_node.on('click', '.select_category', function () {
    $(this).css('background-color', 'white').css('color', '#76839a')
})

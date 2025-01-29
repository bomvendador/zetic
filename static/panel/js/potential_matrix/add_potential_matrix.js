// expand_menu_item('#menu_individual_report_points_description_filters_list')

$('#add_filter_category').on('click', function () {
    let html = $('#category_tr_template').html()
    $('#tbody_filter_categories').append(html)

})

$('#tbody_filter_categories').on('click', '.delete-category-row', function () {
    $(this).closest('tr').remove()
})

$('#description_card_body').on('click', 'textarea', function () {
    $(this).removeClass('is-invalid state-invalid')
})

$('#save_potential_matrix').on('click', function () {
    let categories_ok = true
    let categories_added = true
    let categories_repeat_ok = true
    let square_ok = true
    let points_val_ok = true
    let points_comparison_ok = true
    let categories_val_arr = []
    let categories_arr = []
    let square = $('#square').val()
    console.log(square)
    if (square === '' || square === '0') {
        toastr.error('Выберите квадрат')
        square_ok = false
    }
    $('#tbody_filter_categories tr').each(function (row) {

        let category_val = $(this).find('.select_category option:selected').val()
        if (category_val === '') {
            $(this).remove()
        } else if (jQuery.inArray(category_val, categories_val_arr) === -1) {
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
            if (points_comparison_ok && points_val_ok) {
                categories_arr.push({
                    'category_id': category_val,
                    'points_from': points_from.val(),
                    'points_to': points_to.val(),
                })
            } else {
                categories_ok = false
            }
        } else {
            $(this).find('.select_category').css('background-color', 'red').css('color', 'white')
            categories_repeat_ok = false
            categories_ok = false
        }
    })
    if ($('#tbody_filter_categories tr').length === 0) {
        categories_added = false
        toastr.error('Шкалы не добавлены')
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

    if (categories_ok && square_ok && categories_added) {
        // console.log('save')
        console.log(categories_arr)
        btn_spinner('#save_potential_matrix')
        $.ajax({
            headers: {"X-CSRFToken": token},
            url: url_save_potential_matrix,
            type: 'POST',
            data: JSON.stringify({
                'categories': categories_arr,
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
                if(matrix_id === ''){
                    name_type = 'создана'
                }else {
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
                        if(url_edit_project === ''){
                            window.location.href = url_potential_matrix_list

                        }else {
                            window.location.href = url_edit_project

                        }
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

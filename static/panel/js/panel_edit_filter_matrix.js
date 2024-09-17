expand_menu_item('#menu_matrix_filters_list')

$('#add_filter_category').on('click', function () {
    console.log('ssss')
    $('#tbody_filter_categories').append('<tr> \
        <td>\
            <select class="form-control form-select select_category" data-placeholder="Выберите шкалу"> \
                <option label="--Выберите шкалу--"></option> \
            </select> \
        </td> \
        <td class="point_from"> \
            <input type="number" min="0" max="10" class="form-control points_from">\
        </td>\
        <td>\
            <input type="number" min="0" max="10" class="form-control points_to">\
        </td>\
        <td style="text-align: center; vertical-align: middle;">\
            <div style="float: right">\
                <i class="fe fe-x delete-category-row" style="font-size: 20px; cursor: pointer"></i>\
            </div>\
        </td>\
                    \
    </tr>')

    // categories.forEach(function (category) {
    //
    // })
    let last_tr = $('#tbody_filter_categories tr:last')
    let select_category = last_tr.find('.select_category').eq(0)
    categories.forEach(function (category) {
        select_category.append(`<option value="${category['id']}">${category['code']} - ${category['section_name']} - ${category['category_name']}</option>`)

    })
})

$('#tbody_filter_categories').on('click', '.delete-category-row', function () {
    $(this).closest('tr').remove()
})

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
    let categories_ok = true
    let categories_added = true
    let square_ok = true
    let categories_repeat_ok = true
    let points_val_ok = true
    let points_comparison_ok = true
    let categories_val_arr = []
    let categories_arr = []
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

    $('#tbody_filter_categories tr').each(function (row) {

        let category_val = $(this).find('.select_category option:selected').val()
        if(category_val === ''){
            $(this).remove()
        }else {
            if(jQuery.inArray(category_val,categories_val_arr) === -1){
                // the element is not in the array
                let points_from = $(this).find('.points_from').eq(0)
                let points_to = $(this).find('.points_to').eq(0)
                categories_val_arr.push(category_val)
                if(points_from.val() === ''){
                    points_val_ok = false
                    points_from.css('background-color', 'red').css('color', 'white')
                }
                if(points_to.val() === ''){
                    points_val_ok = false
                    points_to.css('background-color', 'red').css('color', 'white')
                }

                if(points_val_ok){
                    if(Number(points_from.val()) >= Number(points_to.val())){
                        points_comparison_ok = false
                        points_from.css('background-color', 'red').css('color', 'white')
                        points_to.css('background-color', 'red').css('color', 'white')
                    }else {
                        console.log('125')
                    }
                }else {
                    console.log('125')
                }
                if(points_comparison_ok && points_val_ok){
                    categories_arr.push({
                        'category_id': category_val,
                        'points_from': points_from.val(),
                        'points_to': points_to.val(),
                    })
                }else {
                    console.log('216')
                    categories_ok = false
                }
            }else {
                $(this).find('.select_category').css('background-color', 'red').css('color', 'white')
                categories_repeat_ok = false
                categories_ok = false
                console.log('223')
            }
        }
    })
    if($('#tbody_filter_categories tr').length === 0){
        categories_added = false
        toastr.error('Шкалы не добавлены')
    }


    if(!categories_repeat_ok){
        toastr.error('Есть повторяющиеся шкалы')
    }

    if(!points_val_ok){
        toastr.error('Есть пустые баллы')
    }
    if(!points_comparison_ok){
        toastr.error('Баллы ОТ должны быть меньше Баллов ДО')
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
    console.log(`positions_ok - ${positions_ok} categories_ok - ${categories_ok} square_ok - ${square_ok}`)
    // console.log(categories_arr)
    // console.log(positions_arr)

    if(positions_ok && categories_ok && square_ok && categories_added){
        // console.log('save')
        btn_spinner('#save_matrix_filter')
        $.ajax({
            headers: {"X-CSRFToken": token},
            url: url_save_edited_matrix_filter,
            type: 'POST',
            data: JSON.stringify({
                'positions': positions_arr,
                'categories': categories_arr,
                'square': square,
                'filter_id': matrix_filter
            }),
            processData: false,
            contentType: false,
            error: function (data) {
                toastr.error('Ошибка', data)
            },
            success: function (data) {
                console.log(data)
                btn_text('#save_matrix_filter', 'Сохранить фильтр')
                Swal.fire({
                  title: 'Данные сохранены',
                  text: "Фильтр обновлен",
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






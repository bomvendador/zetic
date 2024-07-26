expand_menu_item('#menu_integral_report_filters_list')

$('#add_filter_category').on('click', function () {
    $('#tbody_filter_categories').append('<tr> \
        <td>\
            <select class="form-control form-select select_category" data-placeholder="Выберите шкалу"> \
                <option label="--Выберите шкалу--"></option> \
            </select> \
        </td> \
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


$('#save_edited_integral_report_filter').on('click', function () {
    let categories_ok = true
    let categories_added = true
    let categories_repeat_ok = true
    let name_ok = true
    let categories_val_arr = []
    let categories_arr = []

    let filter_name = $('#input_filter_name').val()
    if (filter_name === '') {
        toastr.error('Название фильтра не заполнено')
        name_ok = false
    }

    $('#tbody_filter_categories tr').each(function (row) {

        let category_val = $(this).find('.select_category option:selected').val()
        if (category_val === '') {
            $(this).remove()
        } else {
            if (jQuery.inArray(category_val, categories_val_arr) === -1) {
                // the element is not in the array
                categories_val_arr.push(category_val)
                categories_arr.push({
                    'category_id': category_val,
                })
            } else {
                $(this).find('.select_category').css('background-color', 'red').css('color', 'white')
                categories_repeat_ok = false
                categories_ok = false
                console.log('223')
            }
        }
    })
    if ($('#tbody_filter_categories tr').length === 0) {
        categories_added = false
        toastr.error('Шкалы не добавлены')
    }


    if (!categories_repeat_ok) {
        toastr.error('Есть повторяющиеся шкалы')
    }

    if (categories_ok && name_ok && categories_added) {
        // console.log('save')
        console.log(categories_arr)
        btn_spinner('#save_integral_report_filter')
        $.ajax({
            headers: {"X-CSRFToken": token},
            url: url_save_edited_integral_report_filter,
            type: 'POST',
            data: JSON.stringify({
                'categories': categories_arr,
                'name': filter_name,
                'filter_id': filter_id
            }),
            processData: false,
            contentType: false,
            error: function (data) {
                toastr.error('Ошибка', data)
            },
            success: function (data) {
                console.log(data)
                btn_text('#save_integral_report_filter', 'Сохранить фильтр')

                let output_html = '<h2 class="mb-0" style="text-align: center">Данные сохранены</h2>' +
                    '<br>' +
                    '<hr class="solid mt-0" style="background-color: black;">' +
                    '<h4 style="text-align: center">Фильтр обновлен</h4>' +
                    '<hr class="solid mt-0" style="background-color: black;">'

                Swal.fire({
                    html: output_html,
                    icon: 'success',
                    confirmButtonColor: '#3085d6',
                    cancelButtonColor: '#d33',
                    confirmButtonText: 'ОК'
                }).then((result) => {
                    if (result.value) {
                        window.location.href = url_integral_report_filters_list
                    }
                })

            }
        })


    }
})

$('#tbody_filter_categories').on('click', '.select_category', function () {
    $(this).css('background-color', 'white').css('color', '#76839a')
})




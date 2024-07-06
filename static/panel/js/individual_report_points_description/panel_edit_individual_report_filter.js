expand_menu_item('#menu_individual_report_points_description_filters_list')

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

$('#description_card_body').on('click', 'textarea', function () {
    $(this).removeClass('is-invalid state-invalid')
})

$('#save_edited_individual_report_description_filter').on('click', function () {
    let categories_ok = true
    let categories_added = true
    let categories_repeat_ok = true
    let name_ok = true
    let points_val_ok = true
    let descriptions_ok = true
    let points_comparison_ok = true
    let categories_val_arr = []
    let categories_arr = []
    let description_text_arr = []

    let filter_name = $('#input_filter_name').val()
    if (filter_name === '') {
        toastr.error('Название фильтра не заполнено')
        name_ok = false
    }

    $('#description_card_body .description-row').each(function (){

        let description_tag = $(this).find('textarea')
        let description_val = description_tag.val()
        if(description_val === ''){
            descriptions_ok = false
            description_tag.addClass('is-invalid state-invalid')
        }else {
            description_text_arr.push(description_val)
        }
        console.log(description_val)
    })

    if(!descriptions_ok){
        toastr.error('Текст описания отсутствует')
    }

    $('#tbody_filter_categories tr').each(function (row) {

        let category_val = $(this).find('.select_category option:selected').val()
        if (category_val === '') {
            $(this).remove()
        } else {
            if (jQuery.inArray(category_val, categories_val_arr) === -1) {
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
                    console.log('216')
                    categories_ok = false
                }
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

    if (!points_val_ok) {
        toastr.error('Есть пустые баллы')
    }
    if (!points_comparison_ok) {
        toastr.error('Баллы ОТ должны быть меньше Баллов ДО')
    }

    if (categories_ok && name_ok && categories_added) {
        // console.log('save')
        console.log(categories_arr)
        btn_spinner('#save_edited_individual_report_description_filter')
        $.ajax({
            headers: {"X-CSRFToken": token},
            url: url_save_edited_individual_report_points_description_filter,
            type: 'POST',
            data: JSON.stringify({
                'categories': categories_arr,
                'name': filter_name,
                'description_text': description_text_arr,
                'filter_id': filter_id,
            }),
            processData: false,
            contentType: false,
            error: function (data) {
                toastr.error('Ошибка', data)
            },
            success: function (data) {
                console.log(data)
                btn_text('#save_edited_individual_report_description_filter', 'Сохранить фильтр')

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
                        window.location.href = url_individual_report_points_description_filters_list
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

$('#description_block').on('click', '.delete-description', function () {
    $(this).closest('.description-row').remove()

})

$('#add_filter_description').on('click', function () {
    let html = '                     <div class="row description-row">\n' +
        '                                <div class="col col-lg-11 col-sm-12" style="">\n' +
        '                                    <textarea class="form-control mb-4"\n' +
        '                                              placeholder="Пункт описания" required="" rows="3"></textarea>\n' +
        '                                </div>\n' +
        '                                <div class="col col-lg-1 col-sm-12" style="">\n' +
        '                                    <div style="text-align: center; vertical-align: middle;">\n' +
        '                                        <div style="float: right; padding-right: 0.73rem" class="delete-description">\n' +
        '                                            <i class="fe fe-x delete-category-row"\n' +
        '                                               style="font-size: 20px; cursor: pointer"></i>\n' +
        '                                        </div>\n' +
        '                                    </div>\n' +
        '                                </div>\n' +
        '                            </div>\n'

    $('#description_card_body').append(html)
})




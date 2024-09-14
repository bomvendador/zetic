expand_menu_item('#menu_settings')

$('.boolean-setting-checkbox').on('click', function () {
    $(this).closest('tr').find('.save-boolean-setting-div').removeClass('d-none')
})

$('.save-boolean-setting-div').on('click', function () {
    let setting_value = $(this).closest('tr').find('.boolean-setting-checkbox').prop('checked')
    let setting_id = $(this).closest('tr').data('setting-id')
    let save_element_div = $(this)
    show_progressbar_loader()
    $.ajax({
        headers: {"X-CSRFToken": token},
        url: url_save_boolean_setting,
        type: 'POST',
        data: JSON.stringify({
            'setting_value': setting_value,
            'setting_id': setting_id,
        }),
        processData: false,
        contentType: false,
        error: function (data) {
            toastr.error('Ошибка', data)
        },
        success: function (data) {
            hide_progressbar_loader()
            toastr.success('Настройка сохранена')
            save_element_div.addClass('d-none')
        }
    })
})
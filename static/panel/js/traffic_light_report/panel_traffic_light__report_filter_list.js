if (project_id === '') {
    expand_menu_item('#menu_settings')
}

// let section_id
//
$('#add_traffic_light_report_filter').on('click', function () {
    if (project_id === '') {
        window.location.href = url_add_traffic_light_report_filter
    } else {
        window.location.href = url_add_traffic_light_report_filter_to_project
    }
})

$('.delete-filter').on('click', function () {
    let filter_id = $(this).closest('tr').data('filter-id')
    console.log(filter_id)

    let output_html = '<h2 class="mb-0" style="text-align: center">Удаление фильтра</h2>' +
        '<br>' +
        '<hr class="solid mt-0" style="background-color: black;">' +
        '<h4 style="text-align: center">Удалить фильтр?</h4>' +
        '<hr class="solid mt-0" style="background-color: black;">'
    Swal.fire({
        html: output_html,
        icon: 'question',
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Да',
        cancelButtonText: 'Нет',
        showCancelButton: true
    }).then((result) => {
        if (result.value) {
            show_progressbar_loader()
            let filter_id = $(this).closest('tr').data('filter-id')
            $.ajax({
                headers: {"X-CSRFToken": token},
                url: url_delete_traffic_light_filter,
                type: 'POST',
                data: JSON.stringify({
                    'filter_id': filter_id
                }),
                processData: false,
                contentType: false,
                error: function (data) {
                    toastr.error('Ошибка', data)
                },
                success: function (data) {
                    hide_progressbar_loader()
                    let output_html = '<h2 class="mb-0" style="text-align: center">Данные сохранены</h2>' +
                        '<br>' +
                        '<hr class="solid mt-0" style="background-color: black;">' +
                        '<h4 style="text-align: center">Фильтр удалён</h4>' +
                        '<hr class="solid mt-0" style="background-color: black;">'

                    Swal.fire({
                        html: output_html,
                        icon: 'success',
                        confirmButtonColor: '#3085d6',
                        cancelButtonColor: '#d33',
                        confirmButtonText: 'ОК'
                    }).then((result) => {
                        if (result.value) {
                            window.location.reload()
                        }
                    })

                }
            })


        }
    })
})

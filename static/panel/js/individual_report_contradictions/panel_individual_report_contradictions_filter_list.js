expand_menu_item('#menu_settings')

// let section_id
//
$('#add_individual_report_contradictions_filter').on('click', function () {
    window.location.href = url_add_individual_report_contradictions_filter
})

$('#wizard1-tbody-1').on('click', '.delete-contradictions-filter', function () {
    let output_html = '<hr class="solid mt-0" style="background-color: black;">' +
        '<h3 style="text-align: center">Удаление фильтра</h3>' +
        '<hr class="solid mt-0" style="background-color: black;">' +
        '<div style="text-align: center">Удалить фильтр?</div>'
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
            let filter_id = $(this).closest('tr').data('filter-id')
            $.ajax({
                headers: {"X-CSRFToken": token},
                url: url_delete_individual_report_contradictions_filter,
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
                    console.log(data)
                    if (data['error']) {
                        Swal.fire({
                            title: 'Ошибка',
                            text: data['error'],
                            icon: 'error',
                            confirmButtonColor: '#3085d6',
                            cancelButtonColor: '#d33',
                            confirmButtonText: 'ОК'
                        })
                    } else {
                        let html = '<hr class="solid mt-0" style="background-color: black;">' +
                            '<h3 style="text-align: center">Фильтр удален</h3>' +
                            '<hr class="solid mt-0" style="background-color: black;">' +
                            '<div style="text-align: center">Данные успешно обновлены</div>'
                        Swal.fire({
                            html: html,
                            icon: 'success',
                            confirmButtonColor: '#3085d6',
                            cancelButtonColor: '#d33',
                            confirmButtonText: 'ОК'
                        }).then((isConfirmed) => {
                            if (isConfirmed) {
                                window.location.reload()
                            }
                        })

                    }
                }
            });
        }
    })

})



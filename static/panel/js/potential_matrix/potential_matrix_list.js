switch (document_type) {
    case 'potential_matrix_list':
        expand_menu_item('#menu_settings')
        break;
    case 'edit_project':
        expand_menu_item('#menu_projects_list')
        break;
    default:
        break;
}


if (document_type === 'potential_matrix_list') {
    if (no_free_matrices) {
        toastr.warning('Все квадраты матрицы уже определены')
    }
    $('#add_potential_matrix').on('click', function () {
        window.location.href = url_add_potential_matrix
    })

}
// let section_id
//

$('body').on('click', '.delete-potential-matrix', function () {
    let output_html = '<hr class="solid mt-0" style="background-color: black;">' +
        '<h3 style="text-align: center">Удаление матрицы</h3>' +
        '<hr class="solid mt-0" style="background-color: black;">' +
        '<div style="text-align: center">Удалить матрицу?</div>'
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
            let matrix_id = $(this).closest('tr').data('matrix-id')
            $.ajax({
                headers: {"X-CSRFToken": token},
                url: url_delete_potential_matrix,
                type: 'POST',
                data: JSON.stringify({
                    'matrix_id': matrix_id
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
                            '<h3 style="text-align: center">Матрица удалена</h3>' +
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
                                switch (document_type) {
                                    case 'potential_matrix_list':
                                        window.location.href = url_potential_matrix_list;
                                        break;
                                    case 'edit_project':
                                        window.location.reload();
                                        break;
                                    default:
                                        break;
                                }
                            }
                        })

                    }
                }
            });
        }
    })

})



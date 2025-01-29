expand_menu_item('#menu_projects_list')



$('#edit_studies').on("click", function (e) {
    show_progressbar_loader()
    $.ajax({
        headers: {"X-CSRFToken": token},
        url: get_company_studies_for_project,
        type: 'POST',
        data: JSON.stringify({
            'company_id': company_id,
        }),
        processData: false,
        contentType: false,
        error: function (data) {
            toastr.error('Ошибка сервера', data)
        },
        success: function (data) {
            hide_progressbar_loader()
            console.log(data)

            if (data === 'no_studies') {
                toastr.warning('Исследования для выбранной компании отсутствуют')
            } else {
                // $('#table_studies').html('')
                $('#modal_table_add_studies').DataTable().destroy()

                $('#tbody_modal_choose_studies_for_project').html(data)
            }

            process_table_clear('#modal_table_add_studies')
            $('#modal_studies').modal('show')

        }
    });

});

$('#add_study_to_project_table').on('click', function () {
    let html_arr = []
    let study_has_been_chosen = false
    $('#tbody_modal_choose_studies_for_project .study_chosen_for_project').each(function (item) {
        if ($(this).prop('checked') === true) {
            study_has_been_chosen = true
            let tr_node = $(this).closest('tr')
            let td_of_tr = []
            let td_nodes = tr_node.find('td')
            let study_id = tr_node.data('study-id')
            td_of_tr.push(study_id)

            td_nodes.each(function (index) {
                if (index !== 0) {
                    td_of_tr.push('<td>' + $(this).html().trim() + '</td>')
                }
            })
            // let tr_html = $(this).closest('tr').html()
            html_arr.push(td_of_tr)
        }

    })
    if (study_has_been_chosen) {
        $('#table_studies').DataTable().destroy()
        let html_for_table_studies = ''
        html_arr.forEach(function (row, index) {
            let tr_html = '<tr data-study-id="' + row[0] + '">'
            row.forEach(function (td, index) {
                if (index > 0) {
                    tr_html = tr_html + td
                }
            })
            tr_html = tr_html + '</tr>'
            // console.log(tr_html)
            html_for_table_studies = html_for_table_studies + tr_html

        })
        //
        $('#tbody_studies').html(html_for_table_studies)

        process_table_clear('#table_studies')
        $('#modal_studies').modal('hide')
        $('#save_project').prop('disabled', false)

    } else {
        toastr.error('Исследование не выбрано')
    }


})


$('#input_project_name').on('click', function () {
    $(this).removeClass('is-invalid')
})

$('#save_project').on('click', function () {
    let study_ids = []
    let name = $('#input_project_name').val()
    if (name === '') {
        toastr.error('Название не заполнено')
        $('#input_project_name').addClass('is-invalid')
    } else {
        $('#tbody_studies tr').each(function (index) {
            let study_id = $(this).data('study-id')
            study_ids.push(study_id)
        })
        btn_spinner('#save_project')
        $.ajax({
            headers: {"X-CSRFToken": token},
            url: url_save_edited_project,
            type: 'POST',
            data: JSON.stringify({
                'study_ids': study_ids,
                'name': name,
                'project_id': project_id
            }),
            processData: false,
            contentType: false,
            error: function (data) {
                toastr.error('Ошибка', data)
            },
            success: function (data) {
                btn_text('#save_project', 'Сохранить проект')
                // hide_progressbar_loader()
                // let employees = data['response']['employees']
                let output_html = '<h2 class="mb-0" style="text-align: center">Данные сохранены</h2>' +
                    '<br>' +
                    '<hr class="solid mt-0" style="background-color: black;">' +
                    '<h4 style="text-align: center">Проект обновлен</h4>' +
                    '<hr class="solid mt-0" style="background-color: black;">'

                Swal.fire({
                    html: output_html,
                    icon: 'success',
                    confirmButtonColor: '#3085d6',
                    cancelButtonColor: '#d33',
                    confirmButtonText: 'ОК'
                }).then((result) => {
                    if (result.isConfirmed) {
                        window.location.href = url_projects_list
                    }
                })

            }
        })

    }

})

$('#add_project').on('click', function () {
    window.location.href = url_add_new_project
})

$('#add_potential_matrix_to_project').on('click', function () {
    console.log('dddd')
    window.location.href = url_add_potential_matrix_for_project
})



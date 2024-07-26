expand_menu_item('#menu_projects_list')


$('#select_company').on("select2:select", function (e) {
    console.log($(this).val())
    let company_id = $(this).val()

    show_progressbar_loader()
    $('#check_all_studies_for_project').prop('checked', false)
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
        $('#save_new_project').prop('disabled', false)

    } else {
        toastr.error('Исследование не выбрано')
    }


})

$('#check_all_studies_for_project').on('click', function () {
    if ($(this).prop('checked') === true) {
        $('#tbody_modal_choose_studies_for_project .study_chosen_for_project').each(function (item) {
            $(this).prop('checked', true)
        })

    } else {
        $('#tbody_modal_choose_studies_for_project .study_chosen_for_project').each(function (item) {
            $(this).prop('checked', false)
        })

    }
})

$('#input_project_name').on('click', function () {
    $(this).removeClass('is-invalid')
})

$('#save_new_project').on('click', function () {
    let study_ids = []
    let name = $('#input_project_name').val()
    let company_id = $('#select_company').val()
    if (name === '') {
        toastr.error('Название не заполнено')
        $('#input_project_name').addClass('is-invalid')
    } else {
        $('#tbody_studies tr').each(function (index) {
            let study_id = $(this).data('study-id')
            study_ids.push(study_id)
        })
        btn_spinner('#save_new_project')
        $.ajax({
            headers: {"X-CSRFToken": token},
            url: url_save_new_project,
            type: 'POST',
            data: JSON.stringify({
                'study_ids': study_ids,
                'name': name,
                'company_id': company_id
            }),
            processData: false,
            contentType: false,
            error: function (data) {
                toastr.error('Ошибка', data)
            },
            success: function (data) {
                btn_text('#save_new_project', 'Сохранить проект')
                // hide_progressbar_loader()
                // let employees = data['response']['employees']
                let output_html = '<h2 class="mb-0" style="text-align: center">Данные сохранены</h2>' +
                    '<br>' +
                    '<hr class="solid mt-0" style="background-color: black;">' +
                    '<h4 style="text-align: center">Проект добавлен</h4>' +
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



expand_menu_item('#menu_filters_list')

// let section_id
//
$('#add_filter').on('click', function () {
    window.location.href = url_add_filter
})

$('.delete-filter').on('click', function () {
    let filter_id = $(this).closest('ul').attr('data-filter-id')
    console.log(filter_id)

    Swal.fire({
        title: 'Удаление фильтра',
        text: "Удалить фильтр?",
        icon: 'question',
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Да',
        cancelButtonText: 'Нет',
        showCancelButton: true
    }).then((result) => {
        if (result.value) {
            $.ajax({
                headers: {"X-CSRFToken": token},
                url: url_delete_filter,
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
                        let output_html = '<hr class="solid mt-0" style="background-color: black;">' +
                        '<div>' + data["error"] + '</div>' +
                        '<br>' +
                        '<hr class="solid mt-0" style="background-color: black;">'

                        Swal.fire({
                            html: output_html,
                            icon: 'error',
                            confirmButtonColor: '#3085d6',
                            cancelButtonColor: '#d33',
                            confirmButtonText: 'ОК'
                        })

                    }
                    Swal.fire({
                        title: 'Фильтр удален',
                        text: "Данные успешено обновлены",
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
            });
        }
    })


})
$('.edit-filter').on('click', function () {
    show_progressbar_loader()
})


//
// $('#save_new_section').on('click', function () {
//     let name = $('#input_section_name').val()
//
//
//     if(name === ''){
//         toastr.error('Название должно быть заполнено')
//     }else {
//         btn_spinner($('#save_new_section'))
//             let name = $('#input_section_name').val()
//             $.ajax({
//                 headers: { "X-CSRFToken": token },
//                 url: url_save_new_section,
//                 type: 'POST',
//                 data: JSON.stringify({
//                             'name': name
//                         }),
//                 processData: false,
//                 contentType: false,
//                 error: function(data){
//                     toastr.error('Ошибка', data)
//                 },
//                 success:function (data) {
//                     console.log(data)
//                     $('#input_modal_add_section').modal('hide')
//                     $('#input_modal_edit_section').modal('hide')
//                     Swal.fire({
//                       title: 'Секция добавлена',
//                       text: "Данные успешено обновлены",
//                       icon: 'success',
//                       confirmButtonColor: '#3085d6',
//                       cancelButtonColor: '#d33',
//                       confirmButtonText: 'ОК'
//                     }).then((isConfirmed) => {
//                       if (isConfirmed) {
//                           window.location.reload()
//                       }
//                     })
//                 }
//             });
//     }
// })
//
//
// $('.edit-section').on('click', function () {
//     section_id = $(this).closest('ul').attr('id').split("_")[2]
//     let name = $(this).closest('tr').find('.section-name-ru').text().trim()
//     $('#input_section_edit_name').val(name)
//
//     $('#input_modal_edit_section').modal('show')
//
// })
//
// $('.delete-section').on('click', function () {
//
//
//     Swal.fire({
//         title: 'Удаление секции',
//         text: "Удалить секцию?",
//         icon: 'question',
//         confirmButtonColor: '#3085d6',
//         cancelButtonColor: '#d33',
//         confirmButtonText: 'Да',
//         cancelButtonText: 'Нет',
//         showCancelButton: true
//     }).then((result) => {
//         if (result.value) {
//             section_id = $(this).closest('ul').attr('id').split("_")[2]
//             $.ajax({
//                 headers: { "X-CSRFToken": token },
//                 url: url_delete_section,
//                 type: 'POST',
//                 data: JSON.stringify({
//                             'section_id': section_id
//                         }),
//                 processData: false,
//                 contentType: false,
//                 error: function(data){
//                     toastr.error('Ошибка', data)
//                 },
//                 success:function (data) {
//                     console.log(data)
//                     $('#input_modal_edit_section').modal('hide')
//                     Swal.fire({
//                       title: 'Секция удалена',
//                       text: "Данные успешено обновлены",
//                       icon: 'success',
//                       confirmButtonColor: '#3085d6',
//                       cancelButtonColor: '#d33',
//                       confirmButtonText: 'ОК'
//                     }).then((isConfirmed) => {
//                       if (isConfirmed) {
//                           window.location.reload()
//                       }
//                     })
//                 }
//             });
//         }
//     })
//
// })
//
//
// $('#edit_section').on('click', function () {
//     let name = $('#input_section_edit_name').val()
//
//     if(name === ''){
//         toastr.error('Название должно быть заполнено')
//     }else {
//
//         btn_spinner($('#edit_section'))
//         $.ajax({
//             headers: { "X-CSRFToken": token },
//             url: url_edit_section,
//             type: 'POST',
//             data: JSON.stringify({
//                         'name': name,
//                         'section_id': section_id
//                     }),
//             processData: false,
//             contentType: false,
//             error: function(data){
//                 toastr.error('Ошибка', data)
//             },
//             success:function (data) {
//                 console.log(data)
//                 $('#input_modal_edit_section').modal('hide')
//                 Swal.fire({
//                   title: 'Секция обновлена',
//                   text: "Данные успешено обновлены",
//                   icon: 'success',
//                   confirmButtonColor: '#3085d6',
//                   cancelButtonColor: '#d33',
//                   confirmButtonText: 'ОК'
//                 }).then((isConfirmed) => {
//                   if (isConfirmed) {
//                       window.location.reload()
//                   }
//                 })
//             }
//         });
//
//
//     }
// })
//
//

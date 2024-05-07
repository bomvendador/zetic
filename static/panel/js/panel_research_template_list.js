// expand_menu_item('#menu_sections_list')

let research_template_id
let sections_for_new_template = []

// $('#add_research_template').on('click', function () {
//     $('#input_modal_add_research_template').modal('show')
// })
$('#add_research_template').on('click', function () {

    show_progressbar_loader()
    $.ajax({
        headers: { "X-CSRFToken": token },
        url: url_get_all_sections,
        type: 'POST',
        data: '',
        processData: false,
        contentType: false,
        error: function(data){
            toastr.error('Ошибка', data)
        },
        success:function (data) {
            hide_progressbar_loader()
            let response = data['response']
            let sections = response['sections']
            $('#section_select').html('')
            sections_for_new_template = []
            sections.forEach(function (section) {
                console.log(section)
                sections_for_new_template.push({
                    'id': section['id'],
                    'name': section['name']
                })
            })

            // btn_text($('#add_research_template_section'), '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">\n' +
            //     '                                            <path d="M8 12H16" stroke="#292D32" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"></path>\n' +
            //     '                                            <path d="M12 16V8" stroke="#292D32" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"></path>\n' +
            //     '                                            <path d="M9 22H15C20 22 22 20 22 15V9C22 4 20 2 15 2H9C4 2 2 4 2 9V15C2 20 4 22 9 22Z" stroke="#292D32" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"></path>\n' +
            //     '                                            </svg>\n' +
            //     '                                            <span style="color: black; margin-left: 5px">Добавить секцию</span>')
        }
    });



    $('#input_modal_add_research_template').modal('show')
    $('#sortable_add').sortable({
        opacity: 0.6,
        cursor: 'move'
    })
})

$('#modal_choose_section').on('hidden.bs.modal', function () {
    $('#input_modal_add_research_template').modal('show')
})
//
$('#add_research_template_section').on('click', function () {
    if(sections_for_new_template.length > 0){
        $('#section_select').html('')
        sections_for_new_template.forEach(function (section){
            $('#section_select').append('<option id="section_id_' + section["id"] + '">' + section["name"] + '</option>')
        })
        // let row_html = $('#new_section_row_template').html()
        // $('#sortable_add').append('<li>' + row_html + '</li>')
        $('#input_modal_add_research_template').modal('hide')
        $('#modal_choose_section').modal('show')

    }else {
        toastr.warning('Все секции уже добавлены')
    }

})




$('#add_section_to_edited_research_template').on('click', function () {
    if(sections_for_new_template.length > 0){
        $('#section_select_edit').html('')
        sections_for_new_template.forEach(function (section){
            $('#section_select_edit').append('<option id="sectionEdit_id_' + section["id"] + '">' + section["name"] + '</option>')
        })
        // let row_html = $('#new_section_row_template').html()
        // $('#sortable_add').append('<li>' + row_html + '</li>')
        $('#input_modal_edit_research_template').modal('hide')
        $('#modal_choose_section_edit').modal('show')

    }else {
        toastr.warning('Все секции уже добавлены')
    }

})

$('#modal_choose_section_edit').on('hidden.bs.modal', function () {
    $('#input_modal_edit_research_template').modal('show')
})


$('#add_section_to_new_research_template').on('click', function () {
    let section_name = $('#section_select option:selected').val()
    let section_id = $('#section_select option:selected').attr('id').split('_')[2]
    console.log(`id-${section_id} name-${section_name}`)
    let row_html = '<li><div class="row mt-2 mb-2 new-section-row section-row">\n' +
        '                <div class="col-1" style="text-align: center; display: flex; align-items: center; -ms-flex-pack: center; justify-content: center;">\n' +
        '                    <i class="fe fe-move" style="font-size: 18px"></i>\n' +
        '                </div>\n' +
        '                <div class="col-10">\n' +
        '                    <input id="section_id_' + section_id + '" type="text" class="form-control section_name_for_new_template" placeholder="Текст ответа" disabled value="' + section_name +  '">\n' +
        '                </div>\n' +
        '                <div class="col-1" style="text-align: center; display: flex; align-items: center; -ms-flex-pack: center; justify-content: center;">\n' +
        '                    <i class="fe fe-x delete-new-template-section-row" style="font-size: 20px; cursor: pointer"></i>\n' +
        '                </div>\n' +
        '            </div></li>\n'
    $('#sortable_add').append(row_html)
    $('#modal_choose_section').modal('hide')
    $('#input_modal_add_research_template').modal('show')
    $('#section_select').html('')
    for(let i in sections_for_new_template){
        console.log(`i = ${sections_for_new_template[i]}`)
        if(sections_for_new_template[Number(i)]['id'] === Number(section_id)){
            sections_for_new_template.splice(Number(i),1);
            break;
        }
    }

})

$('#add_section_to_new_research_template_edit').on('click', function () {
    let section_name = $('#section_select_edit option:selected').val()
    let section_id = $('#section_select_edit option:selected').attr('id').split('_')[2]
    console.log(`id-${section_id} name-${section_name}`)
    let row_html = '<li><div class="row mt-2 mb-2 new-section-row section-row" data-section-id="' + section_id + '">\n' +
        '                <div class="col-1" style="text-align: center; display: flex; align-items: center; -ms-flex-pack: center; justify-content: center;">\n' +
        '                    <i class="fe fe-move" style="font-size: 18px"></i>\n' +
        '                </div>\n' +
        '                <div class="col-10">\n' +
        '                    <input id="section_id_' + section_id + '" type="text" class="form-control section_name_for_new_template" placeholder="Текст ответа" disabled value="' + section_name +  '">\n' +
        '                </div>\n' +
        '                <div class="col-1" style="text-align: center; display: flex; align-items: center; -ms-flex-pack: center; justify-content: center;">\n' +
        '                    <i class="fe fe-x delete-new-template-section-row" style="font-size: 20px; cursor: pointer"></i>\n' +
        '                </div>\n' +
        '            </div></li>\n'
    $('#sortable_edit').append(row_html)
    $('#modal_choose_section_edit').modal('hide')
    // $('#input_modal_add_research_template').modal('show')
    $('#section_select_edit').html('')
    for(let i in sections_for_new_template){
        console.log(`i = ${sections_for_new_template[i]}`)
        if(sections_for_new_template[Number(i)]['id'] === Number(section_id)){
            sections_for_new_template.splice(Number(i),1);
            break;
        }
    }

})


// $('#add_section_to_edited_research_template').on('click', function () {
//     let row_html = $('#new_section_row_template').html()
//     $('#sortable_edit').append('<li>' + row_html + '</li>')
// })

$('#research_template_sections_add_block').on('click', '.delete-new-template-section-row', function () {
    let row = $(this).closest('.new-section-row')
    let id = row.find('.section_name_for_new_template').attr('id').split('_')[2]
    let name = row.find('.section_name_for_new_template').val()
    sections_for_new_template.push({
                    'id': id,
                    'name': name
                })
    row.remove()
})
$('#research_template_sections_edit_block').on('click', '.delete-new-template-section-row', function () {
    let row = $(this).closest('.new-section-row')
    let id = row.find('.section_name_for_new_template').attr('id').split('_')[2]
    let name = row.find('.section_name_for_new_template').val()
    sections_for_new_template.push({
                    'id': id,
                    'name': name
                })
    row.remove()
})
//
// $('#input_modal_edit_question').on('click', '.delete-answer-row', function () {
//
//     $(this).closest('.new-answer-row').remove()
// })
//
// $('#input_modal_add_question').on('hidden.bs.modal', function () {
//     $('#sortable_add').html()
// })
//
// $('#input_modal_edit_question').on('hidden.bs.modal', function () {
//     $('#sortable_edit').html()
// })
//
//
//
$('#save_new_research_template').on('click', function () {
    let test_ok = true
    let sections = []
    let template_name = $('#input_add_research_template_name').val()
    if(template_name === ''){
        toastr.error('Наименование должено быть заполнено')
        test_ok = false
    }

    let sections_qnt = $('.new-section-row').length
    if(sections_qnt === 0){
        toastr.error('В шаблон должна быть добавлена хотя бы одна секция')
        test_ok = false
    }else {
        $('.section_name_for_new_template').each(function () {
            let section_id = $(this).attr('id').split('_')[2]
            sections.push({
                'section_id': section_id,
            })
        })
        console.log(sections)


    }


    if(test_ok){
        btn_spinner($('#save_new_research_template'))
        $.ajax({
            headers: { "X-CSRFToken": token },
            url: url_add_new_research_template,
            type: 'POST',
            data: JSON.stringify({
                'sections': sections,
                'template_name': template_name,
            }),
            processData: false,
            contentType: false,
            error: function(data){
                toastr.error('Ошибка', data)
            },
            success:function (data) {
                console.log(data)
                btn_text($('#save_new_research_template'), 'Сохранить')
                $('#input_modal_add_research_template').modal('hide')
                $('#sortable_add').html('')
                $('#input_add_research_template_text').val('')
                Swal.fire({
                  title: 'Шаблон добавлен',
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

$('#save_edited_template').on('click', function () {
    let test_ok = true
    let sections = []
    let template_name = $('#input_edit_research_template_name').val()
    if(template_name === ''){
        toastr.error('Наименование должено быть заполнено')
        test_ok = false
    }

    let sections_qnt = $('#research_template_sections_edit_block .section-row').length
    if(sections_qnt === 0){
        toastr.error('В шаблон должна быть добавлена хотя бы одна секция')
        test_ok = false
    }else {
        $('#research_template_sections_edit_block .section-row').each(function () {
            let section_id = $(this).attr('data-section-id')
            let template_section_id = $(this).attr('data-template-section-id')
            sections.push({
                'section_id': section_id,
                'template_section_id': template_section_id,
            })
        })
        console.log(sections)
    }
    if(test_ok){
        btn_spinner($('#save_edited_question'))
        $.ajax({
            headers: { "X-CSRFToken": token },
            url: url_edit_research_template,
            type: 'POST',
            data: JSON.stringify({
                'sections': sections,
                'template_name': template_name,
                'template_id': research_template_id
            }),
            processData: false,
            contentType: false,
            error: function(data){
                toastr.error('Ошибка', data)
            },
            success:function (data) {
                Swal.fire({
                  title: 'Шаблон обновлен',
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

// $('#save_edited_question').on('click', function () {
//     let test_ok = true
//     let answers = []
//     let question_edit_text = $('#input_edit_question_text').val()
//     if(question_edit_text === ''){
//         toastr.error('Текст вопроса должен быть заполнен')
//         test_ok = false
//     }
//     $('.answer-row').each(function () {
//         let answer_id;
//         let text = $(this).find('.answer_text').val()
//         let point = $(this).find('.answer_point').val()
//         console.log(`text - ${text} point - ${point}`)
//         if(text === '' || point === ''){
//             toastr.error('Текст ответа и баллы должны быть заполнены')
//             test_ok = false
//         }else {
//             if($(this).hasClass('answer-row-from-db')){
//                 answer_id = $(this).find('.delete-answer-row-from-db').attr('id').split('_')[2]
//             }else {
//                 answer_id = ''
//             }
//             answers.push({
//                 'text': text,
//                 'point': point,
//                 'answer_id': answer_id
//             })
//         }
//     })
//     console.log(answers)
//     if(test_ok){
//         btn_spinner($('#save_edited_question'))
//         let question_id
//         $.ajax({
//             headers: { "X-CSRFToken": token },
//             url: url_edit_question,
//             type: 'POST',
//             data: JSON.stringify({
//                 'question_text': question_edit_text,
//                 'answers': answers,
//                 'question_id': $('#input_modal_edit_question').attr('data-question-id'),
//
//             }),
//             processData: false,
//             contentType: false,
//             error: function(data){
//                 toastr.error('Ошибка', data)
//             },
//             success:function (data) {
//                 // console.log(data)
//                 $('#input_modal_edit_question').modal('hide')
//                 Swal.fire({
//                   title: 'Вопрос изменен',
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
//     }
//
// })


$('.edit-research-template').on('click', function () {
    show_progressbar_loader()
    research_template_id = $(this).closest('ul').attr('id').split("_")[2]
    $.ajax({
        headers: { "X-CSRFToken": token },
        url: url_get_research_template_data,
        type: 'POST',
        data: JSON.stringify({
            'research_template_id': research_template_id,
        }),
        processData: false,
        contentType: false,
        error: function(data){
            toastr.error('Ошибка', data)
        },
        success:function (data) {
            hide_progressbar_loader()
            console.log(data['response'])
            let sections = data['response']['sections']
            let research_template_name = data['response']['research_template_name']
            let research_template_id = data['response']['research_template_id']
            let sections_not_in_template = data['response']['sections_not_in_template']
            // $('#input_modal_edit_question').attr('data-question-id', question_id_)
            $('#input_edit_research_template_name').val(research_template_name)
            let row_html
            $('#sortable_edit').html('')
            sections.forEach(function (section, i) {
                row_html = '<li>     <div class="row mt-2 mb-2 section-row-from-db section-row" data-template-section-id="' + section['research_template_section_id'] + '" >\n' +
                    '                <div class="col-1" style="text-align: center; display: flex; align-items: center; -ms-flex-pack: center; justify-content: center;">\n' +
                    '                    <i class="fe fe-move" style="font-size: 18px"></i>\n' +
                    '                </div>\n' +
                    '                <div class="col-10">\n' +
                    '                    <input type="text" class="form-control" value="' + section['name'] + '" disabled>\n' +
                    '                </div>\n' +
                    '                <div class="col-1" style="text-align: center; display: flex; align-items: center; -ms-flex-pack: center; justify-content: center;">\n' +
                    '                    <i id="templateSection_id_' + section['research_template_section_id'] + '" class="fe fe-trash-2 delete-section-from-research-template-db-row" style="font-size: 20px; cursor: pointer"></i>\n' +
                    '                </div>\n' +
                    '            </div></li>'
                $('#sortable_edit').append(row_html)

            })

            $( "#sortable_edit" ).sortable({
                opacity: 0.6,
                cursor: 'move'
            });
            // $('#input_edit_question_text').val(question_text)
            //
            sections_for_new_template = []
            sections_not_in_template.forEach(function (section) {
                sections_for_new_template.push({
                    'id': section['id'],
                    'name': section['name'],
                })
            })

            $('#input_modal_edit_research_template').modal('show')
        }
    });

})

$('#input_modal_edit_research_template').on('click', '.delete-section-from-research-template-db-row', function () {
    console.log($(this).attr('id'))
    let template_section_id
    Swal.fire({
        title: 'Удаление секции из шаблона',
        text: "Удалить секцию?",
        icon: 'question',
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Да',
        cancelButtonText: 'Нет',
        showCancelButton: true
    }).then((result) => {
        console.log(result.value)
        if (result.value) {
            template_section_id = $(this).attr('id').split('_')[2]
            $.ajax({
                headers: { "X-CSRFToken": token },
                url: url_delete_section_from_template,
                type: 'POST',
                data: JSON.stringify({
                            'template_section_id': template_section_id
                        }),
                processData: false,
                contentType: false,
                error: function(data){
                    toastr.error('Ошибка', data)
                },
                success:function (data) {
                    console.log(data)
                    $('#input_modal_edit_section').modal('hide')
                    if(data['error']){
                        Swal.fire({
                          title: 'Ошибка',
                          text: data['error'],
                          icon: 'error',
                          confirmButtonColor: '#3085d6',
                          cancelButtonColor: '#d33',
                          confirmButtonText: 'ОК'
                        })

                    }else {
                        $(`#templateSection_id_${template_section_id}`).closest('li').remove()

                        Swal.fire({
                          title: 'Секция из шаблона удалена',
                          text: "Данные успешено обновлены",
                          icon: 'success',
                          confirmButtonColor: '#3085d6',
                          cancelButtonColor: '#d33',
                          confirmButtonText: 'ОК'
                        }).then(function () {
                            window.location.reload()
                        })

                    }
                }
            });
        }
    })


})

$('.delete-research-template').on('click', function () {


    Swal.fire({
        title: 'Удаление шаблона',
        text: "Удалить шаблон?",
        icon: 'question',
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Да',
        cancelButtonText: 'Нет',
        showCancelButton: true
    }).then((result) => {
        if (result.value) {
            let template_id = $(this).closest('ul').attr('id').split("_")[2]
            $.ajax({
                headers: { "X-CSRFToken": token },
                url: url_delete_template,
                type: 'POST',
                data: JSON.stringify({
                            'template_id': template_id
                        }),
                processData: false,
                contentType: false,
                error: function(data){
                    toastr.error('Ошибка', data)
                },
                success:function (data) {
                    if(data['error']){
                        Swal.fire({
                          title: 'Ошибка',
                          text: data['error'],
                          icon: 'error',
                          confirmButtonColor: '#3085d6',
                          cancelButtonColor: '#d33',
                          confirmButtonText: 'ОК'
                        })

                    }else {
                        Swal.fire({
                          title: 'Шаблон удален',
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

                }
            });
        }
    })

})





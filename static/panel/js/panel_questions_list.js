// expand_menu_item('#menu_sections_list')

let question_id

$('#add_question').on('click', function () {
    $('#input_modal_add_question').modal('show')
    $('#sortable_add').sortable({
                opacity: 0.6,
                cursor: 'move'
            })
})

$('#input_modal_add_question #add_answer').on('click', function () {
    let row_html = $('#new_answer_row_template').html()
    $('#sortable_add').append('<li>' + row_html + '</li>')

})

$('#input_modal_edit_question #add_answer').on('click', function () {
    let row_html = $('#new_answer_row_template').html()
    $('#sortable_edit').append('<li>' + row_html + '</li>')
})

$('#input_modal_add_question').on('click', '.delete-answer-row', function () {

    $(this).closest('.new-answer-row').remove()
})

$('#input_modal_edit_question').on('click', '.delete-answer-row', function () {

    $(this).closest('.new-answer-row').remove()
})

$('#input_modal_add_question').on('hidden.bs.modal', function () {
    $('#sortable_add').html()
})

$('#input_modal_edit_question').on('hidden.bs.modal', function () {
    $('#sortable_edit').html()
})



$('#save_new_question').on('click', function () {
    let test_ok = true
    let answers = []
    let question_text = $('#input_question_text').val()
    if(question_text === ''){
        toastr.error('Текст вопроса должен быть заполнен')
        test_ok = false
    }

    $('.new-answer-row').each(function () {
        let text = $(this).find('.answer_text').val()
        let point = $(this).find('.answer_point').val()
        console.log(`text - ${text} point - ${point}`)
        if(text === '' || point === ''){
            toastr.error('Текст ответа и баллы должны быть заполнены')
            test_ok = false
        }else {
            answers.push({
                'text': text,
                'point': point,
            })
        }
    })
    console.log(answers)

    if(test_ok){
        btn_spinner($('#save_new_question'))
        $.ajax({
            headers: { "X-CSRFToken": token },
            url: url_add_new_question,
            type: 'POST',
            data: JSON.stringify({
                'question_text': question_text,
                'answers': answers,
                'category_id': category_id,

            }),
            processData: false,
            contentType: false,
            error: function(data){
                toastr.error('Ошибка', data)
            },
            success:function (data) {
                console.log(data)
                $('#input_modal_add_question').modal('hide')
                Swal.fire({
                  title: 'Вопрос добавлен',
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

    // let name = $('#input_section_name').val()
    //
    //
    // if(name === ''){
    //     toastr.error('Название должно быть заполнено')
    // }else {
    //     btn_spinner($('#save_new_section'))
    //         let name = $('#input_section_name').val()
    //         $.ajax({
    //             headers: { "X-CSRFToken": token },
    //             url: url_save_new_section,
    //             type: 'POST',
    //             data: JSON.stringify({
    //                         'name': name
    //                     }),
    //             processData: false,
    //             contentType: false,
    //             error: function(data){
    //                 toastr.error('Ошибка', data)
    //             },
    //             success:function (data) {
    //                 console.log(data)
    //                 $('#input_modal_add_section').modal('hide')
    //                 $('#input_modal_edit_section').modal('hide')
    //                 Swal.fire({
    //                   title: 'Секция добавлена',
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
    // }
})

$('#save_edited_question').on('click', function () {
    let test_ok = true
    let answers = []
    let question_edit_text = $('#input_edit_question_text').val()
    if(question_edit_text === ''){
        toastr.error('Текст вопроса должен быть заполнен')
        test_ok = false
    }
    $('.answer-row').each(function () {
        let answer_id;
        let text = $(this).find('.answer_text').val()
        let point = $(this).find('.answer_point').val()
        console.log(`text - ${text} point - ${point}`)
        if(text === '' || point === ''){
            toastr.error('Текст ответа и баллы должны быть заполнены')
            test_ok = false
        }else {
            if($(this).hasClass('answer-row-from-db')){
                answer_id = $(this).find('.delete-answer-row-from-db').attr('id').split('_')[2]
            }else {
                answer_id = ''
            }
            answers.push({
                'text': text,
                'point': point,
                'answer_id': answer_id
            })
        }
    })
    console.log(answers)
    if(test_ok){
        btn_spinner($('#save_edited_question'))
        let question_id
        $.ajax({
            headers: { "X-CSRFToken": token },
            url: url_edit_question,
            type: 'POST',
            data: JSON.stringify({
                'question_text': question_edit_text,
                'answers': answers,
                'question_id': $('#input_modal_edit_question').attr('data-question-id'),

            }),
            processData: false,
            contentType: false,
            error: function(data){
                toastr.error('Ошибка', data)
            },
            success:function (data) {
                // console.log(data)
                $('#input_modal_edit_question').modal('hide')
                Swal.fire({
                  title: 'Вопрос изменен',
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

    // let name = $('#input_section_name').val()
    //
    //
    // if(name === ''){
    //     toastr.error('Название должно быть заполнено')
    // }else {
    //     btn_spinner($('#save_new_section'))
    //         let name = $('#input_section_name').val()
    //         $.ajax({
    //             headers: { "X-CSRFToken": token },
    //             url: url_save_new_section,
    //             type: 'POST',
    //             data: JSON.stringify({
    //                         'name': name
    //                     }),
    //             processData: false,
    //             contentType: false,
    //             error: function(data){
    //                 toastr.error('Ошибка', data)
    //             },
    //             success:function (data) {
    //                 console.log(data)
    //                 $('#input_modal_add_section').modal('hide')
    //                 $('#input_modal_edit_section').modal('hide')
    //                 Swal.fire({
    //                   title: 'Секция добавлена',
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
    // }
})


$('.edit-question').on('click', function () {
    show_progressbar_loader()
    question_id = $(this).closest('ul').attr('id').split("_")[2]
    $.ajax({
        headers: { "X-CSRFToken": token },
        url: url_get_question_data,
        type: 'POST',
        data: JSON.stringify({
            'question_id': question_id,
        }),
        processData: false,
        contentType: false,
        error: function(data){
            toastr.error('Ошибка', data)
        },
        success:function (data) {
            hide_progressbar_loader()
            console.log(data['response'])
            let answers = data['response']['answers']
            let question_text = data['response']['question_text']
            let question_id_ = data['response']['question_id']
            $('#input_modal_edit_question').attr('data-question-id', question_id_)
            let row_html
            $('#sortable_edit').html('')
            answers.forEach(function (answer, i) {
                row_html = '<li> ' +
                    '<div class="row mt-2 mb-2 answer-row-from-db answer-row">\n' +
                    '                <div class="col-1" style="text-align: center; display: flex; align-items: center; -ms-flex-pack: center; justify-content: center;">\n' +
                    '                    <i class="fe fe-move" style="font-size: 18px"></i>\n' +
                    '                </div>\n' +
                    '                <div class="col-7">\n' +
                    '                    <input type="text" class="form-control answer_text" placeholder="Текст ответа" value="' + answer['text'] + '">\n' +
                    '                </div>\n' +
                    '                <div class="col-3">\n' +
                    '                    <input type="number" class="form-control answer_point" placeholder="Балл" min="0" value="' + answer['point'] + '">\n' +
                    '                </div>\n' +
                    '                <div class="col-1" style="text-align: center; display: flex; align-items: center; -ms-flex-pack: center; justify-content: center;">\n' +
                    '                    <i id="answer_id_' + answer['id'] + '" class="fe fe-trash-2 delete-answer-row-from-db" style="font-size: 18px; cursor: pointer" title="Удалить"></i>\n' +
                    '                </div>\n' +
                    '            </div>\n' +
                    '</li>'
                $('#sortable_edit').append(row_html)

            })

            $( "#sortable_edit" ).sortable({
                opacity: 0.6,
                cursor: 'move'
            });
            $('#input_edit_question_text').val(question_text)

            $('#input_modal_edit_question').modal('show')
            // Swal.fire({
            //   title: 'Вопрос добавлен',
            //   text: "Данные успешено обновлены",
            //   icon: 'success',
            //   confirmButtonColor: '#3085d6',
            //   cancelButtonColor: '#d33',
            //   confirmButtonText: 'ОК'
            // }).then((isConfirmed) => {
            //   if (isConfirmed) {
            //       window.location.reload()
            //   }
            // })
        }
    });



    // let name = $(this).closest('tr').find('.section-name-ru').text().trim()
    // $('#input_section_edit_name').val(name)
    //
    // $('#input_modal_edit_section').modal('show')

})

$('#input_modal_edit_question').on('click', '.delete-answer-row-from-db', function () {
    console.log($(this).attr('id'))
    let answer_id
    Swal.fire({
        title: 'Удаление ответа на вопрос',
        text: "Удалить ответ?",
        icon: 'question',
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Да',
        cancelButtonText: 'Нет',
        showCancelButton: true
    }).then((result) => {
        console.log(result.value)
        if (result.value) {
            answer_id = $(this).attr('id').split('_')[2]
            $.ajax({
                headers: { "X-CSRFToken": token },
                url: url_delete_answer,
                type: 'POST',
                data: JSON.stringify({
                            'answer_id': answer_id
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
                        $(`#answer_id_${answer_id}`).closest('.answer-row-from-db').remove()

                        Swal.fire({
                          title: 'Ответ удален',
                          text: "Данные успешено обновлены",
                          icon: 'success',
                          confirmButtonColor: '#3085d6',
                          cancelButtonColor: '#d33',
                          confirmButtonText: 'ОК'
                        })

                    }
                }
            });
        }
    })


})

$('.delete-question').on('click', function () {


    Swal.fire({
        title: 'Удаление вопроса',
        text: "Удалить вопрос?",
        icon: 'question',
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Да',
        cancelButtonText: 'Нет',
        showCancelButton: true
    }).then((result) => {
        if (result.value) {
            let question_id = $(this).closest('ul').attr('id').split("_")[2]
            $.ajax({
                headers: { "X-CSRFToken": token },
                url: url_delete_question,
                type: 'POST',
                data: JSON.stringify({
                            'question_id': question_id
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
                        Swal.fire({
                          title: 'Вопрос удален',
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





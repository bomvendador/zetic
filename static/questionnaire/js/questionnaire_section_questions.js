$(document).ready(function () {
    $('html, body').animate({scrollTop: '0px'}, 300);

    document.addEventListener("copy", evt => {
        // (B1) CHANGE THE COPIED TEXT IF YOU WANT
        evt.clipboardData.setData("text/plain", "Копирование текста вопросов запрещено");

        // (B2) PREVENT THE DEFAULT COPY ACTION
        evt.preventDefault();
    }, false);
})

$('.question-answer-input').on('click', function () {
    let total_questions = $('.section-question').length
    let total_answers = $('.question-answer-input:checked').length
    // console.log(`вопросы - ${total_questions} ответы - ${total_answers}`)
    if (total_answers === total_questions) {
        $('#save_page_answers').prop('disabled', false)
    }
})

// console.log(questions)

let section_ended = false
let save_page_answers_clicked = false

$('#save_page_answers').on('click', function () {
    save_page_answers_clicked = true
    let answers = []
    btn_spinner($('#save_page_answers'))
    $('.section-question').each(function (index) {
        let question_id = $(this).attr('id').split('_')[2]
        let answer_id = $(this).find('.question-answer-input:checked').eq(0).val()
        answers.push({
            'question_id': question_id,
            'answer_id': answer_id,
        })
    })
    // console.log(answers)
    $.ajax({
        headers: {"X-CSRFToken": csrf_token},
        url: url_save_answers,
        type: 'POST',
        data: JSON.stringify({
            'answers': answers,
            'code': code,
            'section_id': section_id,

        }),
        processData: false,
        contentType: false,
        error: function (data) {
            console.log(data['responseText'])
            toastr.error('Ошибка', data)
            $('#next_btn').text('Далее').attr('disabled', false).css('opacity', 1)
        },
        success: function (data) {
            // btn_text($('#save_page_answers'), 'Далее')
            // if(){
            //
            // }
            // console.log(data)
            let response = data['response']

            console.log(`total_questionnaire_questions_qnt = ${response['total_questionnaire_questions_qnt']}`)

            // if(){
            //
            // }

            if (response['total_questionnaire_answers_qnt'] === response['total_questionnaire_questions_qnt']) {
                let output_html = '<hr class="solid mt-0" style="background-color: black;">' +
                    '<h4 style="text-align: center" class="mb-0"><b>Вы ответили на все вопросы опросника</b></h4>' +
                    '<br>' +
                    '<hr class="solid mt-0" style="background-color: black;">' +
                    '<div style="text-align: center">Отчет отправлен на Вашу почту</div>' +
                    '<div style="text-align: center"><b>' + response['email'] + '</b></div>' +
                    '<br>' +
                    '<hr class="solid mt-0" style="background-color: black;">'
                Swal.fire({
                    html: output_html,
                    icon: 'success',
                    confirmButtonColor: '#3085d6',
                    cancelButtonColor: '#d33',
                    confirmButtonText: 'ОК'
                }).then((result) => {
                    if (result.value) {
                        // $('#back_to_sections_link').click()
                        window.location.href = document.getElementById("back_to_sections_link").getAttribute("href")
                        // window.location.href = `${code}`

                    }
                })

            } else {
                if (response['total_section_questions_qnt'] === response['questions_answered_qnt']) {
                    let output_html = '<hr class="solid mt-0" style="background-color: black;">' +
                        '<div style="text-align: center">Вы ответили на все вопросы в данной секции</div>' +
                        '<br>' +
                        '<hr class="solid mt-0" style="background-color: black;">'
                    Swal.fire({
                        html: output_html,
                        icon: 'success',
                        confirmButtonColor: '#3085d6',
                        cancelButtonColor: '#d33',
                        confirmButtonText: 'ОК'
                    }).then((result) => {
                        if (result.value) {
                            // $('#back_to_sections_link').click()
                            window.location.href = document.getElementById("back_to_sections_link").getAttribute("href")
                            // window.location.href = `${code}`

                        }
                    })
                    section_ended = true
                } else {
                    window.location.reload()

                }

            }


        }
    });

})

// window.onbeforeunload = function () {
//     return "Do you really want to close?";
// };

window.onbeforeunload = function () {
    let total_answers = $('.question-answer-input:checked').length

    if (total_answers > 0 && !section_ended && !save_page_answers_clicked) {
        return 'There is unsaved data.';
    }
    return undefined;
}


$('#conditions_text').on('click', function () {
    $('#modal_conditions_text').modal('show')
})


$('#agree').on('click', function () {
    let status = !$('#terms').prop('checked')
    console.log(status)
    if (status) {
        console.log('tru')
        $('#next_btn').prop('disabled', false).css('opacity', 1)
    } else {
        $('#next_btn').prop('disabled', true).css('opacity', 0.5)
    }
})


$('#next_btn').on('click', function (e) {
    e.preventDefault()
    let test_ok = true
    let name = $('#name').val()
    let year = $('#year option:selected').val()
    let gender_male = $('#gender-male').prop('checked')
    let gender
    if (gender_male) {
        gender = 'Male'
    } else {
        gender = 'Female'
    }
    let role_id = $('#role option:selected').val().split('_')[2]
    let position_id = $('#position option:selected').val().split('_')[2]
    let industry_id = $('#industry option:selected').val().split('_')[2]
    if (name === '') {
        toastr.error('Поле ИМЯ должно быть заполено')
        test_ok = false
    }

    if (test_ok) {
        let data = {
            'name': name,
            'year': year,
            'gender': gender,
            'role_id': role_id,
            'position_id': position_id,
            'industry_id': industry_id,
            'code': code
        }
        $('#next_btn').html('<span class="loader"></span>').attr('disabled', true).css('opacity', 0.5)
        console.log(url_questionnaire_save_participant_data)
        $.ajax({
            headers: {"X-CSRFToken": csrf_token},
            url: url_questionnaire_save_participant_data,
            type: 'POST',
            data: JSON.stringify({
                'data': data
            }),
            processData: false,
            contentType: false,
            error: function (data) {
                console.log(data['responseText'])
                toastr.error('Ошибка', data)
                $('#next_btn').text('Далее').attr('disabled', false).css('opacity', 1)
            },
            success: function (data) {
                $('#next_btn').text('Далее').attr('disabled', false).css('opacity', 1)
                window.location.reload()
                //     console.log(data)
                //     $('#input_modal_edit_section').modal('hide')
                //     if (data['error']) {
                //         Swal.fire({
                //             title: 'Ошибка',
                //             text: data['error'],
                //             icon: 'error',
                //             confirmButtonColor: '#3085d6',
                //             cancelButtonColor: '#d33',
                //             confirmButtonText: 'ОК'
                //         })
                //
                //     } else {
                //         $(`#answer_id_${answer_id}`).closest('.answer-row-from-db').remove()
                //
                //         Swal.fire({
                //             title: 'Ответ удален',
                //             text: "Данные успешено обновлены",
                //             icon: 'success',
                //             confirmButtonColor: '#3085d6',
                //             cancelButtonColor: '#d33',
                //             confirmButtonText: 'ОК'
                //         })
                //
                //     }
            }
        });

        console.log(data)

    }

})

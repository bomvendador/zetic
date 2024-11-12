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

$('.select-field').on('click', function () {
    $(this).removeClass('wrong-select-value')
})

$('#gender_group_block').on('click', function () {
    $(this).removeClass('wrong-select-value')
})

$('#name').on('click', function () {
    $(this).removeClass('wrong-select-value')
})

$('#next_btn').on('click', function (e) {
    e.preventDefault()
    let test_ok = true
    $('.select-field').each(function () {
        let field_val = $(this).val()
        // console.log(field_val)
        if (field_val === '-- Сделайте выбор --') {
            $(this).addClass('wrong-select-value')
            test_ok = false
        }
    })


    let name = $('#name').val()
    let year = $('#year option:selected').val()
    let gender_male = $('#gender-male').prop('checked')
    let gender_female = $('#gender-female').prop('checked')

    if (name === '') {
        test_ok = false
    }

    if (!gender_female && !gender_male) {
        $('#gender_group_block').addClass('wrong-select-value')
        test_ok = false
    }
    let role_id = $('#role option:selected').val().split('_')[2]
    let position_id = $('#position option:selected').val().split('_')[2]
    let industry_id = $('#industry option:selected').val().split('_')[2]
    if (name === '') {
        $('#name').addClass('wrong-select-value')
        test_ok = false
    }
    if (!test_ok) {
        toastr.error('Заполните все поля')
    } else {
        let gender
        if (gender_male) {
            gender = 'Male'
        }
        if (gender_female) {
            gender = 'Female'
        }
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

                if (data === 'tech_works') {
                    console.log(data)
                    let output_html = '<hr class="solid mt-0" style="background-color: black;">' +
                        '<h2 class="mb-0 mt-0" style="text-align: center">Технические работы</h2>' +
                        '<hr class="solid mt-0" style="background-color: black;">' +
                        '<h4 style="text-align: center">На сайте ведутся технические работы</h4>' +
                        '<h4 style="text-align: center">Просим прощения за неудобства </h4>' +
                        '<h4 style="text-align: center">В ближайшее время сервис возобновит свою работу </h4>' +
                        '<hr class="solid mt-0" style="background-color: black;">'


                    Swal.fire({
                        html: output_html,
                        icon: 'warning',
                        confirmButtonColor: '#3085d6',
                        cancelButtonColor: '#d33',
                        confirmButtonText: 'ОК'
                    }).then(function (result) {
                        window.location.reload()
                    })

                } else {
                    window.location.reload()
                }
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

expand_menu_item('#menu_consultant_form_add')

$('#save_new_consultant_form').on('click', function () {
    let special_comments = $('#special_comments').val()
    let risks = $('#risks').val()
    let career_track = $('#career_track').val()
    let test_ok = true

    let resources_names_ok = true
    let resources_names_are_unique = true
    let resources_comments_are_presents = true
    let comments_ok = true
    let resources = []
    let resources_name = []
    $('.resource-row').each(function () {
        let name = $(this).find('.resource-name')
        if (name.val() === '0') {
            resources_names_ok = false
            name.addClass('is-invalid')
        } else {
            if (resources_name.indexOf(name.val()) >= 0) {
                resources_names_are_unique = false
            } else {
                resources_name.push(name.val())
            }
        }
        let resource_comments = []
        let resource_comments_node = $(this).find('.resource-comment')
        resource_comments_node.each(function () {
            if ($(this).val() === '') {
                $(this).addClass('is-invalid')
                comments_ok = false
            } else {
                resource_comments.push($(this).val())
            }
        })
        if (resource_comments.length === 0) {
            resources_comments_are_presents = false
        }
        if (resources_names_ok && resources_names_are_unique && comments_ok) {
            resources.push({
                'name': name.val(),
                'comments': resource_comments,
            })
        }
    })
    if (!resources_names_ok) {
        toastr.error('Выберите названия всех ресурсов')
        test_ok = false
    }
    if (!resources_names_are_unique) {
        toastr.error('Названия ресурсов не должны повторяться')
        test_ok = false

    }
    if (!resources_comments_are_presents) {
        toastr.error('Для каждого ресурса должен быть добавлен хотя бы один комментарий')
        test_ok = false

    }
    if (resources_names_ok && comments_ok && resources_names_are_unique && resources_comments_are_presents && resources.length < 2) {
        toastr.error('Количество ресурсов должно быть не меньше 2')
        test_ok = false

    }

    let growth_zones_names_ok = true
    let growth_zones_names_are_unique = true
    let growth_zones_comments_are_presents = true
    let growth_zones = []
    let growth_zones_name = []
    $('.growth-zone-row').each(function () {
        let name = $(this).find('.growth-zone-name')
        if (name.val() === '0') {
            growth_zones_names_ok = false
            name.addClass('is-invalid')
        } else {
            if (growth_zones_name.indexOf(name.val()) >= 0) {
                growth_zones_names_are_unique = false
            } else {
                growth_zones_name.push(name.val())
            }
        }
        let growth_zone_comments = []
        let growth_zone_comments_node = $(this).find('.growth-zone-comment')
        growth_zone_comments_node.each(function () {
            if ($(this).val() === '') {
                $(this).addClass('is-invalid')
                comments_ok = false
            } else {
                growth_zone_comments.push($(this).val())
            }
        })
        if (growth_zone_comments.length === 0) {
            growth_zones_comments_are_presents = false
        }
        if (growth_zones_names_ok && growth_zones_comments_are_presents && comments_ok) {
            growth_zones.push({
                'name': name.val(),
                'comments': growth_zone_comments,
            })
        }
    })
    if (!growth_zones_names_ok) {
        toastr.error('Выберите названия всех зон роста')
        test_ok = false

    }
    if (!comments_ok) {
        toastr.error('Комментарии не могут быть пустыми')
        test_ok = false

    }
    if (!growth_zones_names_are_unique) {
        toastr.error('Названия зон роста не должны повторяться')
        test_ok = false

    }
    if (!growth_zones_comments_are_presents) {
        toastr.error('Для каждогой зоны роста должен быть добавлен хотя бы один комментарий')
        test_ok = false

    }
    if (growth_zones_names_ok && comments_ok && growth_zones_names_are_unique && growth_zones_comments_are_presents && growth_zones.length < 2) {
        toastr.error('Количество зон роста должно быть не меньше 2')
        test_ok = false

    }

    if (test_ok) {
        btn_spinner('#save_new_consultant_form')
        $.ajax({
            headers: {"X-CSRFToken": token},
            url: url_save_consultant_form,
            type: 'POST',
            data: JSON.stringify({
                'special_comments': special_comments,
                'risks': risks,
                'career_track': career_track,
                'resources': resources,
                'growth_zones': growth_zones,
                'participant_id': participant_id,
                'form_id': form_id,
                'form_type': form_type
            }),
            processData: false,
            contentType: false,
            error: function (data) {
                toastr.error('Ошибка', data)
            },
            success: function (data) {
                btn_text('#save_new_consultant_form', 'Сохранить')
                let output_html = '<h2 class="mb-0" style="text-align: center">Данные сохранены</h2>' +
                    '<br>' +
                    '<hr class="solid mt-0" style="background-color: black;">' +
                    '<h4 style="text-align: center">Анкета добавлена</h4>' +
                    '<hr class="solid mt-0" style="background-color: black;">'

                Swal.fire({
                    html: output_html,
                    icon: 'success',
                    confirmButtonColor: '#3085d6',
                    cancelButtonColor: '#d33',
                    confirmButtonText: 'ОК'
                }).then((result) => {
                    if (result.isConfirmed) {
                        window.location.href = url_add_consultant_form
                    }
                })

            }
        })

    }


})


$('#add_resource').on('click', function () {
    let resource_template_html = $('#resource_row_template').html()
    $('#resource_card_body').append(resource_template_html)
})

$('#resource_card_body').on('click', '.add-resource-comment', function () {
    let resource_comment_template_html = $('#resource_comment_row_template').html()
    $(this).closest('.resource-row').find('.resource-comment-card-body').append(resource_comment_template_html)
})

$('#resource_card_body').on('click', '.delete-resource-comment', function () {
    $(this).closest('.resource-comment-row').remove()
})

$('#resource_card_body').on('click', '.delete-resource', function () {
    $(this).closest('.resource-row').remove()
})

$('#add_growth_zone').on('click', function () {
    let growth_zone_template_html = $('#growth_zone_row_template').html()
    $('#growth_zone_card_body').append(growth_zone_template_html)
})

$('#growth_zone_card_body').on('click', '.add-growth-zone-comment', function () {
    let growth_zone_comment_template_html = $('#growth_zone_comment_row_template').html()
    $(this).closest('.growth-zone-row').find('.growth-zone-comment-card-body').append(growth_zone_comment_template_html)
})

$('#growth_zone_card_body').on('click', '.delete-growth-zone-comment', function () {
    $(this).closest('.growth-zone-comment-row').remove()
})

$('#growth_zone_card_body').on('click', '.delete-growth-zone', function () {
    $(this).closest('.growth-zone-row').remove()
})

$('body').on('click', '.is-invalid', function () {
    $(this).removeClass('is-invalid')
})


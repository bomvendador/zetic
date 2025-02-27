group_parent_node.on('click', '.delete-group', function () {

    if ($(this).closest('.condition-group').attr('id') === 'group_1') {
        toastr.warning('Нельзя удалить коренвую группу')
    } else {
        let output_html = '<hr class="solid mt-0" style="background-color: black;">' +
            '<h3 style="text-align: center">Удаление группы</h3>' +
            '<hr class="solid mt-0" style="background-color: black;">' +
            '<div style="text-align: center">Удалить группу?</div>'
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
                $(this).closest('.condition-group').remove()
            }
        })

    }


})


function add_group(group_parent_node, current_group_node, current_group_panel_body) {
    let group_html = $('#conditions_group_template').html()
    let groups_cnt = group_parent_node.find('.condition-group').length
    let new_id = 'group_' + Number(groups_cnt + 1).toString()
    // let new_id
    // if(new_group_id === ''){
    //     new_id = 'group_' + Number(groups_cnt + 1).toString()
    // }else {
    //     new_id = 'group_' + new_group_id
    // }
    current_group_panel_body.append(group_html)
    current_group_node.find('.condition-group').last().attr('id', new_id)
    let new_group_node = group_parent_node.find('#' + new_id)
    new_group_node.find('.panel-collapse').eq(0).attr('id', new_id + '_content')
    new_group_node.find('.accordion-toggle').eq(0).attr('href', '#' + new_id + '_content')
    new_group_node.data('parent-group-id', current_group_id)
    let level = current_group_node.parents('.condition-group').length + 1
    new_group_node.data('level', level)
    current_group_node.find('#' + current_group_id + '_content').last().addClass('show') //открыть родительскую группу
}

function add_existing_group(group_data) {
    let group_id = group_data['group_id']
    let group_type = group_data['group_type']
    let group_level = group_data['level']
    console.log(group_data)
    // console.log($('#conditions_group_template .condition-group').html())
    let group_template_node = $('#conditions_group_template').html()
    let new_item = $(group_template_node)

    let condition_group_main_node = new_item.find('.condition-group').eq(0)
    let group_type_node = condition_group_main_node.find('.group-type').eq(0)
    if(group_type === 'and'){
        group_type_node.find('option[value="and"]').attr('selected', true)
    }else {
        group_type_node.find('option[value="or"]').attr('selected', true)
    }
    condition_group_main_node.attr('id', 'group_' + group_id).attr('data-level', group_level)
    let group_content_body_node = condition_group_main_node.find('.group-content-body').eq(0)
    if ('group_data_categories' in group_data) {
        let categories_table_html = group_data['categories_table_html'] //сформированный html блок категрий

        group_content_body_node.html(categories_table_html)
        // group_content_body_node.html(new_potential_matrix_category_table_template_node.html())

    }
    if ('parent_group_id' in group_data) {
        condition_group_main_node.attr('data-parent-group-id', `group_${group_data['parent_group_id']}`)
        condition_group_main_node.find('a').eq(0).attr('href', '#group_' + group_id + '_content')
        condition_group_main_node.find('.panel-collapse').eq(0).attr('id', 'group_' + group_id + '_content')
        $('#potential_matrix_conditions_body').find('#group_' + group_data['parent_group_id']).find('.group-content-body').eq(0).append(new_item.html())
    } else {
        $('#potential_matrix_conditions_body .card-body').eq(0).html(new_item.html())
    }
    $('#potential_matrix_conditions_body .panel-collapse').addClass('show')

}

// function add_existing_group(group_parent_node, group_id, parent_group_id, categories) {
//     let group_html = $('#conditions_group_template').html()
//     let groups_cnt = group_parent_node.find('.condition-group').length
//     let new_id
//     if(new_group_id === ''){
//         new_id = 'group_' + Number(groups_cnt + 1).toString()
//     }else {
//         new_id = 'group_' + new_group_id
//     }
//     current_group_panel_body.append(group_html)
//     current_group_node.find('.condition-group').last().attr('id', new_id)
//     let new_group_node = group_parent_node.find('#' + new_id)
//     new_group_node.find('.panel-collapse').eq(0).attr('id', new_id + '_content')
//     new_group_node.find('.accordion-toggle').eq(0).attr('href', '#' + new_id + '_content')
//     new_group_node.data('parent-group-id', current_group_id)
//     let level = current_group_node.parents('.condition-group').length + 1
//     new_group_node.data('level', level)
//     current_group_node.find('#' + current_group_id + '_content').last().addClass('show') //открыть родительскую группу
// }

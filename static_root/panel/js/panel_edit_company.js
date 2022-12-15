expand_menu_item('#menu_companies_list')

$('#add_admin').on('click', function () {

    $.ajax({
        headers: { "X-CSRFToken": token },
        url: url_get_company_employees,
        type: 'POST',
        data: JSON.stringify({
                'company_id': id
            }),
        processData: false,
        contentType: false,
        error: function(data){
            toastr.error('Ошибка', data)
        },
        success:function (data) {
            let data_json = data['data']
            console.log(data_json)

        }
    });





    $('#input_modal_add_admin').modal('show')
})


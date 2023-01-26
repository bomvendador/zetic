
expand_menu_item('#menu_company_add')

let active = 1

$('#company_active').on('click', function () {
    console.log($(this).attr('checked'))
    if ($(this).attr('checked') === 'checked'){
        $(this).attr('checked', false)
        active = 0
    }else {
        $(this).attr('checked', 'checked')
        active = 1
    }
})

    $('#save_company').on('click', function () {
        if($('#input_company_name').val() === ''){
            toastr.error('Название компании не заполнено')
        }else {
            btn_spinner($('#save_company'))
            $.ajax({
                headers: { "X-CSRFToken": token },
                url: url_save_new_company,
                type: 'POST',
                data: JSON.stringify({
                            'name': $('#input_company_name').val(),
                            'active': active
                        }),
                processData: false,
                contentType: false,
                error: function(data){
                    toastr.error('Ошибка', data)
                },
                success:function (data) {
                    console.log(data)
                    Swal.fire({
                      title: 'Компания создана',
                      text: "Данные компании успешено сохранены",
                      icon: 'success',
                      confirmButtonColor: '#3085d6',
                      cancelButtonColor: '#d33',
                      confirmButtonText: 'ОК'
                    }).then((result) => {
                      if (result.isConfirmed) {
                          window.location.href = url_panel_home
                      }
                    })
                }
            });
        }
    })

function save_company_parameter(dict, url_save, modal_selector, swal_title, swal_text) {

    $.ajax({
        headers: { "X-CSRFToken": token },
        url: url_save, //url_save_new_industry
        type: 'POST',
        data: JSON.stringify(dict),
        processData: false,
        contentType: false,
        error: function(data){
            toastr.error('Ошибка', data)
        },
        success:function (data) {
            if (modal_selector !== ''){
                $(modal_selector).modal('hide') //'#input_modal_add_industry'
            }
            if(swal_text !== ''){
                Swal.fire({
                  title: swal_title,
                  text: swal_text,
                  icon: 'success',
                  confirmButtonColor: '#3085d6',
                  cancelButtonColor: '#d33',
                  confirmButtonText: 'ОК'
                }).then((result) => {
                  if (result.isConfirmed) {
                      window.location.reload()
                  }
                })

            }else {
                window.location.reload()

            }
        }
    });
}


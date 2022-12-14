expand_menu_item('#menu_companies_list')

$('.edit-company').one('click', function () {
    let company_id = $(this).closest('ul').attr('id').split('_')[2].trim()
    window.location.href = 'company/' + company_id
})
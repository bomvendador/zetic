expand_menu_item('#menu_statistics_report_1')

$.fn.bootstrapdatepicker.dates['ru'] = {
    days: ["Воскресенье", "Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"],
    daysShort: ["Вс", "Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"],
    daysMin: ["Вс", "Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"],
    months: ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"],
    monthsShort: ["Янв", "Фев", "Мар", "Апр", "Май", "Июн", "Июл", "Авг", "Сен", "Окт", "Ноя", "Дек"],
    today: "Сегодня"
};
$('.datepicker-date').bootstrapdatepicker({
    format: "dd-mm-yyyy",
    viewMode: "date",
    language: 'ru',
    weekStart: 1
})

$('#statistics_reports_report_type_select_filter').on('change', function () {
    let selected_filter = $(this).val()

    if (selected_filter !== current_filter_selected) {
        switch (selected_filter) {
            case 'report_1':
                window.location.href = url_statistics_report_1;
                break;
            case 'report_2':
                window.location.href = url_statistics_report_2;
                break;
            default:
                break;

        }
    }
})


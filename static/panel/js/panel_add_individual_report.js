expand_menu_item('#menu_individual_reports_add')

window.onerror = function myErrorHandler(errorMsg, url, lineNumber){
    toastr.error('Ошибка - все поля должны быть заполнены')
    return false;
}

     $("#parse_file").on("click", function () {
        //Reference the FileUpload element.
         $('.error-message-close-btn').each(function (i, e) {
             e.click()
         })
        let fileUpload = $("#files")[0];

        //Validate whether File is valid Excel file.
        let regex = /^([а-яА-Яa-zA-Z0-9\s_\\.\-:])+(.xls|.xlsx|.xlsm)$/;
        if (regex.test(fileUpload.value.toLowerCase())) {
            if (typeof (FileReader) != "undefined") {
                let reader = new FileReader();

                //For Browsers other than IE.
                if (reader.readAsBinaryString) {
                    reader.onload = function (e) {
                        ProcessExcel(e.target.result);
                    };
                    reader.readAsBinaryString(fileUpload.files[0]);
                } else {
                    //For IE Browser.
                    reader.onload = function (e) {
                        let data = "";
                        let bytes = new Uint8Array(e.target.result);
                        for (let i = 0; i < bytes.byteLength; i++) {
                            data += String.fromCharCode(bytes[i]);
                        }
                        ProcessExcel(data);
                    };
                    reader.readAsArrayBuffer(fileUpload.files[0]);
                }
            } else {
                toastr.error("Браузер не поддерживает HTML5.");
            }
        } else {
            toastr.error('Загрузите корректный файл')
        }
    });

    function ProcessExcel(data) {
        //Read the Excel File data.
        let workbook = XLSX.read(data, {
            type: 'binary'
        });

        //Fetch the name of First Sheet.
        let sheet_exists = false
        let sheets = workbook.SheetNames;
        let sheet
        for (let i = 0; i < sheets.length; i++) {
            console.log('sheet - ' + sheets[i])

            if(sheets[i] === 'ДАННЫЕ'){
                sheet = sheets[i]
                sheet_exists = true
            }
        }
        console.log(sheet_exists)
        // console.log(firstSheet)
        if (sheet_exists){
            //Read all rows from First Sheet into an JSON array.
            sheet = workbook.Sheets[sheet]
            // let range = XLSX.utils.decode_range(sheet)
            // let cell_ref = XLSX.utils.encode_cell({c:8, r:3})
            console.log(sheet['K4'])
            let participant_name = sheet['I3'].v
            let email = sheet['K3'].v
            let study_name = sheet['K4'].v
            let company_name = sheet['K5'].v
            let birth_year = sheet['I4'].v
            let gender = sheet['I5'].v
            let lie_points = Math.round(sheet['I7'].v)

            if (email === '' || study_name === '' || company_name === ''){
                let output_html = '<hr class="solid mt-0" style="background-color: black;">' +
                                '<div>Имя участника, Email, Название опросника и Навзание компании должны быть заполнены</div>' +
                                '<br>' +
                                '<hr class="solid mt-0" style="background-color: black;">'
                Swal.fire({
                  html: output_html,
                  icon: 'warning',
                  confirmButtonColor: '#3085d6',
                  cancelButtonColor: '#d33',
                  confirmButtonText: 'ОК'
                })
            }
            //КЕТТЕЛ
            let kettel = {
                '1_1': sheet['O13'].v,
                '1_2': sheet['O14'].v,
                '1_3': sheet['O15'].v,
                '1_4': sheet['O17'].v,
                '1_5': sheet['O18'].v,
                '1_6': sheet['O19'].v,
                '1_7': sheet['O20'].v,
                '1_8': sheet['O22'].v,
                '1_9': sheet['O23'].v,
                '1_10': sheet['O24'].v,
                '1_11': sheet['O25'].v,
                '1_12': sheet['O27'].v,
                '1_13': sheet['O28'].v,
                '1_14': sheet['O29'].v,
                '1_15': sheet['O30'].v
                }

            //КОПИНГИ
            let kopingi = {
                '2_1': sheet['K12'].v,
                '2_2': sheet['K13'].v,
                '2_3': sheet['K14'].v,
                '2_4': sheet['K16'].v,
                '2_5': sheet['K17'].v,
                '2_6': sheet['K19'].v,
                '2_7': sheet['K20'].v,
                '2_8': sheet['K21'].v,
                '2_9': sheet['K22'].v,
                '2_10' : sheet['K23'].v,
                '2_11' : sheet['K25'].v,
                '2_12' : sheet['K26'].v,
                '2_13' : sheet['K27'].v,
                '2_14' : sheet['K28'].v,
                '2_15' : sheet['K29'].v,
                '2_16' : sheet['K30'].v
                }

            //ВЫГОРАНИЕ
            let boyko = {
                '3_1': sheet['K34'].v,
                '3_2': sheet['K35'].v,
                '3_3': sheet['K36'].v,
                '3_4': sheet['K37'].v,
                '3_5': sheet['K38'].v,
                '3_6': sheet['K39'].v,
                '3_7': sheet['K40'].v,
                '3_8': sheet['K41'].v,
                '3_9': sheet['K42'].v,
                '3_10': sheet['K43'].v,
                '3_11': sheet['K44'].v,
                '3_12': sheet['K45'].v
            }
            //ЦЕННОСТИ
            let values = {
                '4_1': sheet['K48'].v,
                '4_2': sheet['K49'].v,
                '4_3': sheet['K50'].v,
                '4_4': sheet['K51'].v,
                '4_5': sheet['K52'].v,
                '4_6': sheet['K53'].v,
                '4_7': sheet['K54'].v,
                '4_8': sheet['K55'].v,
                '4_9': sheet['K56'].v,
                '4_10': sheet['K57'].v
            }

            let study_id = sheet['K6'].v

            let request = JSON.stringify(
                {
                      "code": "",
                      "lang": "ru",
                      "participant_info": {
                        "name": participant_name,
                        "sex": gender,
                        "year": birth_year,
                        "email": email
                      },
                      "lie_points": lie_points,
                      "study": {
                        "name": "ОПРОСНИК ZETIC 3.1",
                        "id": study_id
                      },
                      "appraisal_data": [
                        {
                          "section": "Копинги",
                          "code": 2,
                          "point": [
                            {"category":"Самообладание", "points": kopingi['2_1'], "code": "2_1"},
                            {"category":"Контроль над ситуацией", "points":kopingi['2_2'], "code": "2_2"},
                            {"category":"Позитивная самомотивация", "points": kopingi['2_3'], "code": "2_3"},
                            {"category":"Снижение значения стрессовой ситуации", "points": kopingi['2_4'], "code": "2_4"},
                            {"category":"Самоутверждение", "points": kopingi['2_5'], "code": "2_5"},
                            {"category":"Отвлечение", "points": kopingi['2_6'], "code": "2_6"},
                            {"category":"Бегство от стрессовой ситуации", "points": kopingi['2_7'], "code": "2_7"},
                            {"category":"Антиципирующее избегание", "points": kopingi['2_8'], "code": "2_8"},
                            {"category":"Замещение", "points": kopingi['2_9'], "code": "2_9"},
                            {"category":"Поиск социальной поддержки", "points": kopingi['2_10'], "code": "2_10"},
                            {"category":"Жалость к себе", "points": kopingi['2_11'], "code": "2_11"},
                            {"category":"Социальная замкнутость", "points": kopingi['2_12'], "code": "2_12"},
                            {"category":"Самообвинение", "points": kopingi['2_13'], "code": "2_13"},
                            {"category": "Заезженная пластинка", "points": kopingi['2_14'], "code": "2_14"},
                            {"category":"Самооправдание", "points": kopingi['2_15'], "code": "2_15"},
                            {"category":"Агрессия", "points": kopingi['2_16'], "code": "2_16"}
                          ]
                        },
                        {
                          "section": "Выгорание Бойко",
                          "code": 3,
                          "point": [
                            {"category":"Напряжение_Переживание", "points": boyko['3_1'], "code": "3_1"},
                            {"category":"Напряжение_Неудовлетворенность собой", "points":boyko['3_2'], "code": "3_2"},
                            {"category":"Напряжение_Загнанность в клетку", "points": boyko['3_3'], "code": "3_3"},
                            {"category":"Напряжение_Тревога", "points": boyko['3_4'], "code": "3_4"},
                            {"category":"Сопротивление_Избирательное реагирование", "points": boyko['3_5'], "code": "3_5"},
                            {"category":"Сопротивление_Эмоциональная защита", "points": boyko['3_6'], "code": "3_6"},
                            {"category":"Сопротивление_Экономия эмоций", "points": boyko['3_7'], "code": "3_7"},
                            {"category":"Сопротивление_Эмпатическая усталость", "points": boyko['3_8'], "code": "3_8"},
                            {"category":"Истощение_Эмоциональная опустошенность", "points": boyko['3_9'], "code": "3_9"},
                            {"category":"Истощение_Эмоциональная отстраненность", "points": boyko['3_10'], "code": "3_10"},
                            {"category":"Истощение_Личностная отстраненность", "points": boyko['3_11'], "code": "3_11"},
                            {"category":"Истощение_Психосоматика", "points":boyko['3_12'], "code": "3_12"}
                          ]
                        },
                        {
                          "section": "Ценности",
                          "code": 4,
                          "point": [
                            {"category":"Причастность", "points": Math.round(values['4_1']), "code": "4_1" },
                            {"category":"Традицонализм", "points":Math.round(values['4_2']), "code": "4_2"},
                            {"category":"Жажда впечатлений", "points": Math.round(values['4_3']), "code": "4_3"},
                            {"category":"Эстетичность", "points": Math.round(values['4_4']), "code": "4_4"},
                            {"category":"Гедонизм", "points": Math.round(values['4_5']), "code": "4_5"},
                            {"category":"Признание", "points": Math.round(values['4_6']), "code": "4_6"},
                            {"category":"Достижения", "points": Math.round(values['4_7']), "code": "4_7"},
                            {"category":"Коммерческий подход", "points": Math.round(values['4_8']), "code": "4_8"},
                            {"category":"Безопасность", "points": Math.round(values['4_9']), "code": "4_9"},
                            {"category":"Интеллект", "points": Math.round(values['4_10']), "code": "4_10"}
                          ]
                        },
                        {
                          "section": "Кеттелл",
                          "code": 1,
                          "point": [
                            {"category":"Шкала C", "points": kettel['1_1'], "code": "1_1"},
                            {"category":"Шкала O", "points":kettel['1_2'], "code": "1_2"},
                            {"category":"Шкала Q4", "points": kettel['1_3'], "code": "1_3"},
                            {"category":"Шкала F", "points": kettel['1_4'], "code": "1_4"},
                            {"category":"Шкала N", "points": kettel['1_5'], "code": "1_5"},
                            {"category":"Шкала I", "points": kettel['1_6'], "code": "1_6"},
                            {"category":"Шкала A", "points": kettel['1_7'], "code": "1_7"},
                            {"category":"Шкала M", "points": kettel['1_8'], "code": "1_8"},
                            {"category":"Шкала Q2", "points": kettel['1_9'], "code": "1_9"},
                            {"category":"Шкала G", "points": kettel['1_10'], "code": "1_10"},
                            {"category":"Шкала Q3", "points": kettel['1_11'], "code": "1_11"},
                            {"category":"Шкала Q1", "points": kettel['1_12'], "code": "1_12"},
                            {"category":"Шкала L", "points": kettel['1_13'], "code": "1_13"},
                            {"category":"Шкала H", "points": kettel['1_14'], "code": "1_14"},
                            {"category":"Шкала E", "points": kettel['1_15'], "code": "1_15"}
                          ]
                        }
                      ]
                    })

            console.log(request)
                    btn_spinner($('#parse_file'))
                    $.ajax({
                        headers: { "X-CSRFToken": token },
                        url: url_json,
                        type: 'POST',
                        data: request,
                        processData: false,
                        contentType: false,
                        error: function(data){
                            toastr.error('Ошибка', data)
                        },
                        success:function (data) {
                            console.log(data)
                            toastr.success('Данные сохранены')
                            btn_text($('#parse_file'), 'Загрузить')

                        }
                    });

        }else {
            toastr.error('Лист "ДАННЫЕ" в файле осутствует')
        }
    }

    // $('#parse_file').on('click', handleFileSelect(document.getElementById('files')))

function show_error_message(text){
        let html_template = $('#template_error_block').html()
        let html_block = html_template.replace('message_text', text)
    // $('.error_message').text(text)
    $('#error_block').append(html_block)
}

from typing import Dict

TRANSLATIONS = {
    "report": {
        "ru": "Индивидуальный отчет",
        "en": "Personal report",
    },
    "participant": {
        "ru": "Участник:",
        "en": "Participant:",
    },
    "zetic": {
        "ru": "Опросник Zetic 4S",
        "en": "Zetic 4S Questionnaire",
    },
    "Introduction": {
        "ru": "Введение",
        "en": "Introduction",
    },
    "Introduction_text": {
        "en": (
            "Based on decades of academic research Zetic has developed a tool for scientific personality measurement "
            "for business. The tool can be used for a variety of recruitment and development purposes. The approach "
            "was tested on a large sample of executives over several years. Our study of resilience and stress "
            "behavior has become the largest in Russia over the past 15 years. Zetic 4S questionnaire consists of:"
        ),
        "ru": (
            "Для разработки опросника ZETIC-4S был использован ряд иностранных и российских психологических "
            "исследований. Подход был переработан под бизнес-контекст и апробирован на большой выборке руководителей."
        ),
    },
    "Introduction_text_2": {
        "en": """
• The section K measures the basic personality traits and its influence of business behavior and performance.
• The section С describes the basic reactions on stress, actions taken by a person to cope with the new worries, to adapt to tension and to find a way out of a traumatic situation.
• The section B reflects the psychological factors that lead to burnout, the burnout indicator and intensity.
• The section V describes the universal well-established needs and life priorities of the individual that influence decisions and choices.
""",
        "ru": """
• Cекция «Базовые черты личности» построена исходя из 5-факторной диспозициональной модели личности, отражающей восприятие людей друг другом. В ее основе - лексический подход, использующий факторный анализ словесных описаний характеристик человека; язык может отразить аспекты личности, которые описывают адаптацию человека к социальной среде с учетом его личных особенностей. Авторы: Г. Олпорт, П. Коста и Р. Маккрэй и Р. Кэттел. 1985-1992г.
• Секция «Поведение в стрессе» сформирована исходя из модели психологического преодоления стресса, описывающей базовые реакции и действия, предпринимаемые человеком, чтобы справиться с переживанием, адаптироваться к нагрузке и найти выход из травмирующей ситуации. Автор: Ричард Лазарус, 1991г.
• Секция «Факторы выгорания» построена на основе модели многофакторного эмоционального выгорания, описывающей механизмы психической защиты и переход в состояние физического и психического истощения, возникающее в ответ на эмоциональное перенапряжение.  Авторы: Б. Фрейденберг, К. Маслач 1992г.
• Секция «Жизненные ценности» разработана на основе модели жизненных ценностей личности, описывающей универсальные устоявшиеся потребности и жизненные приоритеты личности, определяющие условия и порядок принятия личностью важных решений и реализации действий.  Авторы: Ш. Шварц, 1992г.
""",
    },
    "How to read the report": {
        "ru": "Как читать отчет",
        "en": "How to read the report",
    },
    "How to read the report_text": {
        "ru": (
            "Данные исследования описывают индивидуальный профиль устойчивости. Отчет помогает обозначить особенности "
            "реагирования на ситуации неопределенности или стресса, выявить черты личности, влияющие на рабочее поведение "
            "в сложных условиях. В данном отчете результаты сравниваются с нормативной группой русскоговорящих лидеров. "
            "Информация, содержащаяся в этом документе, является конфиденциальной. Отчет необходимо хранить в соответствии "
            "с принципами защиты персональных данных. Срок достоверности отчета — 2 года."
        ),
        "en": (
            "These studies describe an individual resistance profile. The report helps to identify the features of "
            "response to uncertainty and stress and to release personality traits that affect behavior within though "
            "working conditions. In this report, the results are compared with a normative group of Russian-speaking "
            "leaders of the same age and gender comparing to the participant. The information contained in this document "
            "is confidential. The report need to be stored in accordance with the  personal data protection principles. "
            "The report validity period – 2 years."
        ),
    },
    "The scales": {
        "ru": "Шкалы",
        "en": "The scales",
    },
    "The scales_text": {
        "ru": (
            "Результаты в отчете показаны в шкале стенов от 0 до 10 (от английского «стандартная десятка»). Стен означает, "
            "что 10 процентам самых низких результатов среди участников, заполнивших опросник в своей категории, присваивается 1 стен, "
            "а 90 процентов самых выраженных результатов получают 9 стен. Чем выше стен, тем ярче Вы проявляете определенное поведение. "
            "Под каждой шкалой указаны «полюсные» характеристики. Обратите внимание, что не существует «плохого» и «хорошего» поведения. "
            "Каждый «полюс» указывает на особенность характера, имеет свои преимущества и ограничения."
        ),
        "en": (
            "The results in the report are presented with sten scores (an abbreviation for 'Standard Ten').  The lowest "
            "10 percent of the participants who completed the questionnaire in their category are assigned 1 sten, and the "
            "top 90 percent receive 9 stens. The higher score makes the stronger behavior. Each trait is bipolar, there is no "
            "'bad' and 'good' behavior. Each pole indicates a trait that has its own strengths and limitations."
        ),
    },
    "Validity": {
        "ru": "Валидность отчёта",
        "en": "Validity",
    },
    "Validity_text": {
        "ru": (
            "Значения, находящиеся в пределах красной рамки (слишком высокие), "
            "свидетельствуют о разнице в восприятии между желаемым (правильном) поведении и текущих возможностях"
        ),
        "en": (
            "The values within the red frame (are too high) correspond to insincerity, demonstrative behavior and "
            "need for social approval."
        ),
    },
}

DEFAULT_LANG = "en"


class TranslationDict:
    def __init__(self, translations: Dict[str, Dict[str, str]]):
        self._dict = translations

    def get_translation(self, key: str, lang: str = DEFAULT_LANG):
        if lang in self._dict[key]:
            return self._dict[key][lang]
        else:
            return self._dict[key][DEFAULT_LANG]


TRANSLATIONS_DICT = TranslationDict(TRANSLATIONS)

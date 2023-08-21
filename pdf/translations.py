import textwrap
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
        "en": """\
• The section K measures the basic personality traits and its influence of business behavior and performance.
• The section С describes the basic reactions on stress, actions taken by a person to cope with the new worries, to adapt to tension and to find a way out of a traumatic situation.
• The section B reflects the psychological factors that lead to burnout, the burnout indicator and intensity.
• The section V describes the universal well-established needs and life priorities of the individual that influence decisions and choices.""",
        "ru": """\
• Cекция «Базовые черты личности» построена исходя из 5-факторной диспозициональной модели личности, отражающей восприятие людей друг другом. В ее основе - лексический подход, использующий факторный анализ словесных описаний характеристик человека; язык может отразить аспекты личности, которые описывают адаптацию человека к социальной среде с учетом его личных особенностей. Авторы: Г. Олпорт, П. Коста и Р. Маккрэй и Р. Кэттел. 1985-1992г.
• Секция «Поведение в стрессе» сформирована исходя из модели психологического преодоления стресса, описывающей базовые реакции и действия, предпринимаемые человеком, чтобы справиться с переживанием, адаптироваться к нагрузке и найти выход из травмирующей ситуации. Автор: Ричард Лазарус, 1991г.
• Секция «Факторы выгорания» построена на основе модели многофакторного эмоционального выгорания, описывающей механизмы психической защиты и переход в состояние физического и психического истощения, возникающее в ответ на эмоциональное перенапряжение.  Авторы: Б. Фрейденберг, К. Маслач 1992г.
• Секция «Жизненные ценности» разработана на основе модели жизненных ценностей личности, описывающей универсальные устоявшиеся потребности и жизненные приоритеты личности, определяющие условия и порядок принятия личностью важных решений и реализации действий.  Авторы: Ш. Шварц, 1992г.""",
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
    "scale_min": {
        "ru": "Слабо выражено",
        "en": "Weakly expressed",
    },
    "scale_max": {
        "ru": "Ярко выражено",
        "en": "Strongly expressed",
    },
    ## Cattell
    "Section K": {
        "ru": "Базовые черты личности",
        "en": "Section K",
    },
    "Section K_text": {
        "ru": (
            "Приведенные ниже результаты исследования отражают фундаментальные черты личности, определяющие стиль "
            "деятельности и взаимоотношения с окружением. Обнаружив эти черты, Вы можете осознанно усиливать или ослаблять их"
        ),
        "en": (
            "The scores reflect the fundamental personality traits that determine business performance and relationship "
            "attitude. By discovering these traits, you can consciously strengthen or weaken them, increasing your effectiveness."
        ),
    },
    "Emotional stability": {
        "ru": "Эмоциональная устойчивость",
        "en": "Emotional stability",
    },
    "Team resilience": {
        "ru": "Командная устойчивость",
        "en": "Team resilience",
    },
    "Stability of the results": {
        "ru": "Устойчивость результата",
        "en": "Stability of the results",
    },
    "Resilience to change": {
        "ru": "Устойчивость в изменениях",
        "en": "Resilience to change",
    },
    "1_1": {
        "ru": textwrap.dedent(
            """\
            Шкала С
            Эмоциональная
            стабильность"""
        ),
        "en": textwrap.dedent(
            """\
            Scale C
            Emotional
            stability"""
        ),
    },
    "1_1_min": {
        "ru": textwrap.dedent(
            """\
            Следование эмоциям,
            Утомляемость"""
        ),
        "en": textwrap.dedent(
            """\
            Affection by feelings,
            Fatigue, s"""
        ),
    },
    "1_1_max": {
        "ru": textwrap.dedent(
            """\
            Стабильность, Зрелость,
            Работоспособность"""
        ),
        "en": textwrap.dedent(
            """\
            Stability, Maturity,
            Workability"""
        ),
    },
    "1_1_group_desc": {
        "ru": textwrap.dedent(
            """\
            Управление своим состоянием,
            обладание личной зрелостью
            и стабильностью"""
        ),
        "en": textwrap.dedent(
            """\
            """
        ),
    },
    "1_2": {
        "ru": textwrap.dedent(
            """\
            Шкала O
            Тревожность"""
        ),
        "en": textwrap.dedent(
            """\
            Scale O
            Apprehension"""
        ),
    },
    "1_2_min": {
        "ru": textwrap.dedent(
            """\
            Безмятежность,
            Энергичность"""
        ),
        "en": textwrap.dedent(
            """\
            Self-assureness, free of guilt,
            Untroubleness, Energy"""
        ),
    },
    "1_2_max": {
        "ru": textwrap.dedent(
            """\
            Чувство вины, Тревожность,
            Впечатлительность"""
        ),
        "en": textwrap.dedent(
            """\
            Self-blaming, Anxiety,
            Impressionability"""
        ),
    },
    "1_2_group_desc": {
        "ru": textwrap.dedent(
            """\
            Склонность к беспокойству,
            тревоге, вине, повышенной
            требовательности к себе"""
        ),
        "en": textwrap.dedent(
            """\
            """
        ),
    },
    "1_3": {
        "ru": textwrap.dedent(
            """\
        Шкала Q4
        Внутреннее напряжение"""
        ),
        "en": textwrap.dedent(
            """\
        Scale Q4
        Tension"""
        ),
    },
    "1_3_min": {
        "ru": textwrap.dedent(
            """\
    Расслабленность,
    Низкая амбициозность"""
        ),
        "en": textwrap.dedent(
            """\
    Relaxation, Tranquility,
    Low drive,  Composure"""
        ),
    },
    "1_3_max": {
        "ru": textwrap.dedent(
            """\
    Собранность, Напряженность,
    Раздражительность"""
        ),
        "en": textwrap.dedent(
            """\
    Tension, Overthought,
    High drive, Irritability"""
        ),
    },
    "1_3_group_desc": {
        "ru": textwrap.dedent(
            """\
        Внутренняя расслабленность,
        нетерпеливость, мотивация"""
        ),
        "en": "",
    },
    "1_4": {
        "ru": textwrap.dedent(
            """\
    Шкала F
    Импульсивность"""
        ),
        "en": textwrap.dedent(
            """\
    Scale F
    Impulsiveness"""
        ),
    },
    "1_4_min": {
        "ru": textwrap.dedent(
            """\
    Молчаливость,
    Расчетливость"""
        ),
        "en": textwrap.dedent(
            """\
    Taciturnity, Prudence,
    Temperance"""
        ),
    },
    "1_4_max": {
        "ru": textwrap.dedent(
            """\
    Беззаботность, Беспечность,
    Экспрессивность"""
        ),
        "en": textwrap.dedent(
            """\
    Carelessness, Enthusiasm,
    Expressiveness"""
        ),
    },
    "1_4_group_desc": {
        "ru": textwrap.dedent(
            """\
        Экспрессивность, яркость,
        энергичность, активное
        проявление себя в мире"""
        ),
        "en": "",
    },
    "1_5": {
        "ru": textwrap.dedent(
            """\
    Шкала N
    Дипломатичность"""
        ),
        "en": textwrap.dedent(
            """\
    Scale N
    Diplomacy"""
        ),
    },
    "1_5_min": {
        "ru": textwrap.dedent(
            """\
    Прямолинейность,
    Четкость"""
        ),
        "en": textwrap.dedent(
            """\
    Straightforwardness,
    Tactlessness, Genuiness"""
        ),
    },
    "1_5_max": {
        "ru": textwrap.dedent(
            """\
    Влияние,
    Хитрость"""
        ),
        "en": textwrap.dedent(
            """\
    Social awareness,
    Influence, Cunning"""
        ),
    },
    "1_5_group_desc": {
        "ru": textwrap.dedent(
            """\
            Склонность к оказанию влияния,
            построению коммуникаций через
            эмпатию, утонченность"""
        ),
        "en": "",
    },
    "1_6": {
        "ru": textwrap.dedent(
            """\
        Шкала I
        Восприятие"""
        ),
        "en": textwrap.dedent(
            """\
        Scale I
         Sensitivity"""
        ),
    },
    "1_6_min": {
        "ru": textwrap.dedent(
            """\
    Рассудительность, Циничность,
    Ответственность"""
        ),
        "en": textwrap.dedent(
            """\
    Cynicism, Tough-mind,
    Self-reliance"""
        ),
    },
    "1_6_max": {
        "ru": textwrap.dedent(
            """\
    Эмпатичность,
    Интуитивность"""
        ),
        "en": textwrap.dedent(
            """\
    Tender-mind, Empathy,
    Intuitiveness"""
        ),
    },
    "1_6_group_desc": {
        "ru": textwrap.dedent(
            """\
            Эмпатия, восприятие мира через
            ощущения, сентиментальность"""
        ),
        "en": "",
    },
    "1_7": {
        "ru": textwrap.dedent(
            """\
        Шкала A
        Открытость"""
        ),
        "en": textwrap.dedent(
            """\
        Scale A
        Warmth"""
        ),
    },
    "1_7_min": {
        "ru": textwrap.dedent(
            """\
    Замкнутость, Холодность,
    Безучастность, Строгость"""
        ),
        "en": textwrap.dedent(
            """\
    Reserveness, Coldness,
    Indifference, Severity"""
        ),
    },
    "1_7_max": {
        "ru": textwrap.dedent(
            """\
    Общительность,
    Открытость"""
        ),
        "en": textwrap.dedent(
            """\
    Sociability, Warmth,
    Kindness, Openness"""
        ),
    },
    "1_7_group_desc": {
        "ru": textwrap.dedent(
            """\
            Готовность к новым знакомствам,
            приветливость, теплота
            коммуникации, уживчивость"""
        ),
        "en": "",
    },
    "1_8": {
        "ru": textwrap.dedent(
            """\
        Шкала M
        Концептуальность"""
        ),
        "en": textwrap.dedent(
            """\
        Scale M
        Abstractedness"""
        ),
    },
    "1_8_min": {
        "ru": textwrap.dedent(
            """\
    Практичность,
    Реалистичность, Прозаичность"""
        ),
        "en": textwrap.dedent(
            """\
    Practicality, Integrity,
    Realism, Grounding"""
        ),
    },
    "1_8_max": {
        "ru": textwrap.dedent(
            """\
    Восторженность,
    Концептуальность"""
        ),
        "en": textwrap.dedent(
            """\
    Abstracteness, Imagination,
    Idea-oriention"""
        ),
    },
    "1_8_group_desc": {
        "ru": textwrap.dedent(
            """\
            Богатое воображение,склонность
            к концептуализации, яркость
            проявления"""
        ),
        "en": "",
    },
    "1_9": {
        "ru": textwrap.dedent(
            """\
        Шкала Q2
        Автономность"""
        ),
        "en": textwrap.dedent(
            """\
        Scale Q2
        Self-reliance"""
        ),
    },
    "1_9_min": {
        "ru": textwrap.dedent(
            """\
    Зависимость от группы,
    Разделение ответственности"""
        ),
        "en": textwrap.dedent(
            """\
    Group-dependence,
    Division of responsibility"""
        ),
    },
    "1_9_max": {
        "ru": textwrap.dedent(
            """\
    Самостоятельность,
    Независимость"""
        ),
        "en": textwrap.dedent(
            """\
    Independence,
    Resourcefulness"""
        ),
    },
    "1_9_group_desc": {
        "ru": textwrap.dedent(
            """\
            Независимость взглядов и мнений,
            самостоятельность в решениях
            и действиях"""
        ),
        "en": "",
    },
    "1_10": {
        "ru": textwrap.dedent(
            """\
        Шкала G
        Ответственность"""
        ),
        "en": textwrap.dedent(
            """\
        Scale G
        Rule-consciousness"""
        ),
    },
    "1_10_min": {
        "ru": textwrap.dedent(
            """\
    Непостоянство, Ненадежность"""
        ),
        "en": textwrap.dedent(
            """\
    Volatility, Insecurity,
    Expediency"""
        ),
    },
    "1_10_max": {
        "ru": textwrap.dedent(
            """\
    Настойчивость,
    Дисциплина, Долг"""
        ),
        "en": textwrap.dedent(
            """\
    Perseverance, Conformity
    Discipline, Obligation"""
        ),
    },
    "1_10_group_desc": {
        "ru": textwrap.dedent(
            """\
            Воля и выдержка, решимость,
            обязательность, ответственность,
            следование социальным нормам"""
        ),
        "en": "",
    },
    "1_11": {
        "ru": textwrap.dedent(
            """\
            Шкала Q3
            Самоконтроль"""
        ),
        "en": textwrap.dedent(
            """\
            Scale Q3
            Self-control"""
        ),
    },
    "1_11_min": {
        "ru": textwrap.dedent(
            """\
    Конфликтность,
    Невнимательность"""
        ),
        "en": textwrap.dedent(
            """\
    Self-conflict, Disorder Tolerance,
    Inattention"""
        ),
    },
    "1_11_max": {
        "ru": textwrap.dedent(
            """\
    Самоконтроль,
    Сильная воля, Точность"""
        ),
        "en": textwrap.dedent(
            """\
    Self control
    Strong will, Accuracy"""
        ),
    },
    "1_11_group_desc": {
        "ru": textwrap.dedent(
            """\
            Дисциплина, точное следование
            социальным требованиям,
            забота о репутации"""
        ),
        "en": "",
    },
    "1_12": {
        "ru": textwrap.dedent(
            """\
            Шкала Q1
            Критичность"""
        ),
        "en": textwrap.dedent(
            """\
            Scale Q1
            Critical thinking"""
        ),
    },
    "1_12_min": {
        "ru": textwrap.dedent(
            """\
        Интуитивные решения"""
        ),
        "en": textwrap.dedent(
            """\
    Judgement-orientation
    Change intolerance, Conservatism"""
        ),
    },
    "1_12_max": {
        "ru": textwrap.dedent(
            """\
    Экспериментирование,
    Анализ информации"""
        ),
        "en": textwrap.dedent(
            """\
    Information analysis, Criticality
    Work optimization"""
        ),
    },
    "1_12_group_desc": {
        "ru": textwrap.dedent(
            """\
            Склонность к подробному изучению
            информации, исследованию новых
            областей, изучению возможностей
            для оптимизации работы"""
        ),
        "en": "",
    },
    "1_13": {
        "ru": textwrap.dedent(
            """\
        Шкала L
        Осторожность"""
        ),
        "en": textwrap.dedent(
            """\
    Scale L
    Vigilance"""
        ),
    },
    "1_13_min": {
        "ru": textwrap.dedent(
            """\
    Доверчивость, Терпимость,
    Откровенность"""
        ),
        "en": textwrap.dedent(
            """\
    Confidence, Tolerance
    Frankness"""
        ),
    },
    "1_13_max": {
        "ru": textwrap.dedent(
            """\
    Подозрительность,
    Осторожность"""
        ),
        "en": textwrap.dedent(
            """\
    Suspicion
    Caution"""
        ),
    },
    "1_13_group_desc": {
        "ru": textwrap.dedent(
            """\
            Подозрительность,
            раздражительность,
            недоверие к информации"""
        ),
        "en": "",
    },
    "1_14": {
        "ru": textwrap.dedent(
            """\
        Шкала H
        Смелость"""
        ),
        "en": textwrap.dedent(
            """\
        Scale H
        Social boldness"""
        ),
    },
    "1_14_min": {
        "ru": textwrap.dedent(
            """\
    Робость, Деликатность"""
        ),
        "en": textwrap.dedent(
            """\
    Timidity, Delicacy"""
        ),
    },
    "1_14_max": {
        "ru": textwrap.dedent(
            """\
    Смелость, Авантюрность"""
        ),
        "en": textwrap.dedent(
            """\
    Courage, Boldness
    Adventurism"""
        ),
    },
    "1_14_group_desc": {
        "ru": textwrap.dedent(
            """\
            Склонность к авантюризму,
            предприимчивость"""
        ),
        "en": "",
    },
    "1_15": {
        "ru": textwrap.dedent(
            """\
        Шкала E
        Лидерство"""
        ),
        "en": textwrap.dedent(
            """\
        Scale E
        Dominance"""
        ),
    },
    "1_15_min": {
        "ru": textwrap.dedent(
            """\
    Мягкость, Тактичность,
    Уступчивость"""
        ),
        "en": textwrap.dedent(
            """\
    Softness, Tact
    Compliance"""
        ),
    },
    "1_15_max": {
        "ru": textwrap.dedent(
            """\
    Напористость, Властность,
    Самоуверенность"""
        ),
        "en": textwrap.dedent(
            """\
    Assertiveness, Dominance
    Self-confidence"""
        ),
    },
    "1_15_group_desc": {
        "ru": textwrap.dedent(
            """\
            Желание лидировать,
            доминирование, неуступчивость"""
        ),
        "en": "",
    },
    # Coping
    "Section C": {
        "ru": "Поведение в стрессе и неопределенности",
        "en": "Section C",
    },
    "Section C_text": {
        "ru": (
            "Ниже приведены результаты исследования, отражающие наиболее типичные реакции и действия в ситуации стресса "
            "или высокой неопределенности. Изучив свои стратегии поведения, Вы можете изменить их, осознанно действовать "
            "иначе, повышая личную эффективность."
        ),
        "en": (
            "The following scores reflect the most typical reactions and actions under stressful situations or uncertainty. "
            "Having studied your behavioral strategies, you can change them, consciously act differently, increasing your "
            "personal effectiveness."
        ),
    },
    # Coping Categories
    "Problem-focused": {
        "ru": "Стратегии, направленные на активный поиск выхода и преодоление сложностей",
        "en": "Strategies to actively find a way out and overcome difficulties",
    },
    "Emotion-focused": {
        "ru": "Стратегии, направленные на игнорирование проблемы и отказ искать выход из ситуации",
        "en": "Strategies for ignoring problems and avoiding solutions research",
    },
    "Dysfunctional": {
        "ru": "Стратегии, провоцирующие дальнейшее нахождение в стрессе и усиление переживаний",
        "en": "Strategies leading to further stress and strengthening worries",
    },
    # Coping Scales
    "2_1": {
        "ru": textwrap.dedent(
            """\
            Самообладание"""
        ),
        "en": textwrap.dedent(
            """\
            Response control"""
        ),
    },
    "2_1_group_desc": {
        "ru": textwrap.dedent(
            """\
            Контроль собственных
            реакций,чрезмерная
            требовательность к себе"""
        ),
        "en": textwrap.dedent(
            """\
            """
        ),
    },
    "2_2": {
        "ru": textwrap.dedent(
            """\
            Контроль над ситуацией"""
        ),
        "en": textwrap.dedent(
            """\
            Situation control"""
        ),
    },
    "2_2_group_desc": {
        "ru": textwrap.dedent(
            """\
            Поиск и реализация решений
            для преодоления проблемы"""
        ),
        "en": textwrap.dedent(
            """\
            """
        ),
    },
    "2_3": {
        "ru": textwrap.dedent(
            """\
            Позитивная
            самомотивация"""
        ),
        "en": textwrap.dedent(
            """\
            Positive
            self-affirmation"""
        ),
    },
    "2_3_group_desc": {
        "ru": textwrap.dedent(
            """\
            Приписывание себе
            способности управлять
            ситуацией"""
        ),
        "en": textwrap.dedent(
            """\
            """
        ),
    },
    "2_4": {
        "ru": textwrap.dedent(
            """\
            Снижение значения
            стрессовой ситуации"""
        ),
        "en": textwrap.dedent(
            """\
            Stress minimization"""
        ),
    },
    "2_4_group_desc": {
        "ru": textwrap.dedent(
            """\
            Снижение значения или
            тяжести напряжения
            (рационализация, юмор,
            обесценивание)"""
        ),
        "en": textwrap.dedent(
            """\
            """
        ),
    },
    "2_5": {
        "ru": textwrap.dedent(
            """\
            Самоутверждение"""
        ),
        "en": textwrap.dedent(
            """\
            Self-assertion"""
        ),
    },
    "2_5_group_desc": {
        "ru": textwrap.dedent(
            """\
            Получение признания от
            других, самоутверждение
            в иной области"""
        ),
        "en": textwrap.dedent(
            """\
            """
        ),
    },
    # Emotion-focused
    "2_6": {
        "ru": textwrap.dedent(
            """\
            Отвлечение"""
        ),
        "en": textwrap.dedent(
            """\
            Distraction"""
        ),
    },
    "2_6_group_desc": {
        "ru": textwrap.dedent(
            """\
            Отвлечение от стрессовой
            ситуаций"""
        ),
        "en": textwrap.dedent(
            """\
            """
        ),
    },
    "2_7": {
        "ru": textwrap.dedent(
            """\
            Бегство от стрессовой
            ситуации"""
        ),
        "en": textwrap.dedent(
            """\
            Escape"""
        ),
    },
    "2_7_group_desc": {
        "ru": textwrap.dedent(
            """\
            Отказ от преодоления ситуации,
            отрицание/игнорирование
            проблемы, уклонение от
            ответственности, нетерпение"""
        ),
        "en": textwrap.dedent(
            """\
            """
        ),
    },
    "2_8": {
        "ru": textwrap.dedent(
            """\
            Антиципирующее
            избегание"""
        ),
        "en": textwrap.dedent(
            """\
            Avoidance"""
        ),
    },
    "2_8_group_desc": {
        "ru": textwrap.dedent(
            """\
            Попытка предотвратить
            аналогичные стрессовые
            ситуации в будущем"""
        ),
        "en": textwrap.dedent(
            """\
            """
        ),
    },
    "2_9": {
        "ru": textwrap.dedent(
            """\
            Замещение"""
        ),
        "en": textwrap.dedent(
            """\
            Replacement"""
        ),
    },
    "2_9_group_desc": {
        "ru": textwrap.dedent(
            """\
            Обращение к позитивным
            аспектам; создание
            комфортной среды для
            себя и команды"""
        ),
        "en": textwrap.dedent(
            """\
            """
        ),
    },
    "2_10": {
        "ru": textwrap.dedent(
            """\
            Поиск социальной
            поддержки"""
        ),
        "en": textwrap.dedent(
            """\
            Need for
            Social Support"""
        ),
    },
    "2_10_group_desc": {
        "ru": textwrap.dedent(
            """\
            Стремление быть
            выслушанным, разделить
            с кем-либо переживания"""
        ),
        "en": textwrap.dedent(
            """\
            """
        ),
    },
    # Dysfunctional
    "2_11": {
        "ru": textwrap.dedent(
            """\
            Жалость к себе"""
        ),
        "en": textwrap.dedent(
            """\
            Self-pity"""
        ),
    },
    "2_11_group_desc": {
        "ru": textwrap.dedent(
            """\
            Пребывание в жалости к себе,
            зависти к другим;
            недооценивание собственных
            сил и возможностей"""
        ),
        "en": textwrap.dedent(
            """\
            """
        ),
    },
    "2_12": {
        "ru": textwrap.dedent(
            """\
            Социальная
            замкнутость"""
        ),
        "en": textwrap.dedent(
            """\
            Social
            withdrawal"""
        ),
    },
    "2_12_group_desc": {
        "ru": textwrap.dedent(
            """\
            Избегание социальных контактов,
            самоизоляция от
            коммуникации/информации
            """
        ),
        "en": textwrap.dedent(
            """\
            """
        ),
    },
    "2_13": {
        "ru": textwrap.dedent(
            """\
            Самообвинение"""
        ),
        "en": textwrap.dedent(
            """\
            Self-blame"""
        ),
    },
    "2_13_group_desc": {
        "ru": textwrap.dedent(
            """\
            Обвинение себя в
            произошедшем,
            поиск причин в себе"""
        ),
        "en": textwrap.dedent(
            """\
            """
        ),
    },
    "2_14": {
        "ru": textwrap.dedent(
            """\
            «Заезженная
            пластинка»"""
        ),
        "en": textwrap.dedent(
            """\
            Rumination"""
        ),
    },
    "2_14_group_desc": {
        "ru": textwrap.dedent(
            """\
            Постоянное мысленное
            прокручивание аспектов
            стрессовой ситуации"""
        ),
        "en": textwrap.dedent(
            """\
            """
        ),
    },
    "2_15": {
        "ru": textwrap.dedent(
            """\
            Самооправдание"""
        ),
        "en": textwrap.dedent(
            """\
            Denial of guilt"""
        ),
    },
    "2_15_group_desc": {
        "ru": textwrap.dedent(
            """\
            Отказ от ответственности,
            отказ от поиска решения"""
        ),
        "en": textwrap.dedent(
            """\
            """
        ),
    },
    "2_16": {
        "ru": textwrap.dedent(
            """\
            Агрессия"""
        ),
        "en": textwrap.dedent(
            """\
            Aggression"""
        ),
    },
    "2_16_group_desc": {
        "ru": textwrap.dedent(
            """\
            Пребывание в состоянии
            " "сопротивления, ярость/агрессия"""
        ),
        "en": textwrap.dedent(
            """\
            """
        ),
    },
    "2_17": {
        "ru": textwrap.dedent(
            """\
            Замещение, отвлечение, бегство от стресса"""
        ),
        "en": textwrap.dedent(
            """\
            Distraction, avoidance, escape"""
        ),
    },
    "2_17_group_desc": {
        "ru": textwrap.dedent(
            """\
            2_17_group_desc"""
        ),
        "en": textwrap.dedent(
            """\
            """
        ),
    },
    "2_18": {
        "ru": textwrap.dedent(
            """\
            Позитивная мотивация и снижение стресса"""
        ),
        "en": textwrap.dedent(
            """\
            Positive affirmation and stress minimization"""
        ),
    },
    "2_18_group_desc": {
        "ru": textwrap.dedent(
            """\
            2_18_group_desc"""
        ),
        "en": textwrap.dedent(
            """\
            """
        ),
    },
    "2_19": {
        "ru": textwrap.dedent(
            """\
            Самообвинение и жалость к себе"""
        ),
        "en": textwrap.dedent(
            """\
            Self-pity and blame"""
        ),
    },
    "2_19_group_desc": {
        "ru": textwrap.dedent(
            """\
            2_19_group_desc"""
        ),
        "en": textwrap.dedent(
            """\
            """
        ),
    },
    "2_20": {
        "ru": textwrap.dedent(
            """\
            Самообладание и самоутверждение"""
        ),
        "en": textwrap.dedent(
            """\
            Response control и self-assertion"""
        ),
    },
    "2_20_group_desc": {
        "ru": textwrap.dedent(
            """\
            2_20_group_desc"""
        ),
        "en": textwrap.dedent(
            """\
            """
        ),
    },
    # Burnout / Boyko
    "Section B": {
        "en": "Section B",
        "ru": "Факторы профессионального выгорания",
    },
    "Section B_text": {
        "ru": (
            "Ниже приведено исследование механизмов выгорания и степень эмоциональной вовлеченности в работу. Вы "
            "можете увидеть, какие факторы формируют каждую фазу выгорания и в какой точке Вы находитесь прямо сейчас."
        ),
        "en": (
            "The following scores describe the mechanisms of emotional burnout – a consistent decrease in emotional "
            "response to work situations. You can explore behavioral markers shaping burnout phase."
        ),
    },
    "Phase 1. Tension": {
        "ru": textwrap.dedent(
            """\
            Фаза 1. Напряжение"""
        ),
        "en": textwrap.dedent(
            """\
            Phase 1. Tension"""
        ),
    },
    "Phase 2. Resistance": {
        "ru": textwrap.dedent(
            """\
             Фаза 2. Сопротивление   """
        ),
        "en": textwrap.dedent(
            """\
            Phase 2. Resistance"""
        ),
    },
    "Phase 3. Exhaustion": {
        "ru": textwrap.dedent(
            """\
            Фаза 3. Истощение"""
        ),
        "en": textwrap.dedent(
            """\
            Phase 3. Exhaustion"""
        ),
    },
    "3_1": {
        "ru": textwrap.dedent(
            """\
            Переживание"""
        ),
        "en": textwrap.dedent(
            """\
            Concern"""
        ),
    },
    "3_1_group_desc": {
        "ru": textwrap.dedent(
            """\
            Ощущение дискомфорта
            в работе, раздражение
            при решении стандартных
            рабочих задач"""
        ),
        "en": textwrap.dedent(
            """\
            Concern"""
        ),
    },
    "3_2": {
        "ru": textwrap.dedent(
            """\
            Неудовлетворенность
            собой"""
        ),
        "en": textwrap.dedent(
            """\
            Self dissatisfaction"""
        ),
    },
    "3_2_group_desc": {
        "ru": textwrap.dedent(
            """\
            Недовольство собой и
            ситуацией, потребность
            сменить условия работы,
            ощущение"""
        ),
        "en": textwrap.dedent(
            """\
            Concern"""
        ),
    },
    "3_3": {
        "ru": textwrap.dedent(
            """\
            «Загнанность в
            клетку»"""
        ),
        "en": textwrap.dedent(
            """\
            Feeling trapped"""
        ),
    },
    "3_3_group_desc": {
        "ru": textwrap.dedent(
            """\
            Ощущение невозможности
            изменить ситуацию,
            бессилие; отсутствие
            энергии, ощущение
            пустоты внутри"""
        ),
        "en": textwrap.dedent(
            """\
            Concern"""
        ),
    },
    "3_4": {
        "ru": textwrap.dedent(
            """\
            Тревога"""
        ),
        "en": textwrap.dedent(
            """\
            Anxiety"""
        ),
    },
    "3_4_group_desc": {
        "ru": textwrap.dedent(
            """\
            Эмоциональное напряжение,
            ощущение тревоги и
            беспричинного беспокойства,
            желание «остановиться»ч"""
        ),
        "en": textwrap.dedent(
            """\
            Concern"""
        ),
    },
    "3_5": {
        "ru": textwrap.dedent(
            """\
            Избирательное
            реагирование"""
        ),
        "en": textwrap.dedent(
            """\
            Selective emotional
            response"""
        ),
    },
    "3_5_group_desc": {
        "ru": textwrap.dedent(
            """\
            Зависимость коммуникации
            от настроения («хочу или
            не хочу»), эмоциональная
            черствость, равнодушиеч"""
        ),
        "en": textwrap.dedent(
            """\
            Concern"""
        ),
    },
    "3_6": {
        "ru": textwrap.dedent(
            """\
            Эмоциональная
            защита"""
        ),
        "en": textwrap.dedent(
            """\
            Emotional
            defense"""
        ),
    },
    "3_6_group_desc": {
        "ru": textwrap.dedent(
            """\
            Эмоциональная защита,
            неготовность принимать
            на себя дополнительные
            эмоции и справляться
            с ними"""
        ),
        "en": textwrap.dedent(
            """\
            Concern"""
        ),
    },
    # 3_7 - 3_12
    "3_7": {
        "ru": textwrap.dedent(
            """\
            Экономия эмоций"""
        ),
        "en": textwrap.dedent(
            """\
            Emotional saving"""
        ),
    },
    "3_7_group_desc": {
        "ru": textwrap.dedent(
            """\
            Перенос защиты на другие
            сферы жизни (общение с
            близкими, семьей),
            потребность в изоляции
            от других людей"""
        ),
        "en": textwrap.dedent(
            """\
            Concern"""
        ),
    },
    "3_8": {
        "ru": textwrap.dedent(
            """\
            Эмпатическая
            усталость"""
        ),
        "en": textwrap.dedent(
            """\
            Empathic fatigue""",
        ),
    },
    "3_8_group_desc": {
        "ru": textwrap.dedent(
            """\
            Попытки облегчить или
            сократить обязанности,
            требующие эмоциональных
            затрат или эмоционального
            вовлечения"""
        ),
        "en": textwrap.dedent(
            """\
            Concern"""
        ),
    },
    "3_9": {
        "ru": textwrap.dedent(
            """\
            Эмоциональная
            опустошенность"""
        ),
        "en": textwrap.dedent(
            """\
            Emotional
            emptiness""",
        ),
    },
    "3_9_group_desc": {
        "ru": textwrap.dedent(
            """\
            Избегание эмоционального
            ответа на важные ситуации
            и коммуникации"""
        ),
        "en": textwrap.dedent(
            """\
            Concern"""
        ),
    },
    "3_10": {
        "ru": textwrap.dedent(
            """\
            Эмоциональная
            отстраненность"""
        ),
        "en": textwrap.dedent(
            """\
            Emotional
            detachment""",
        ),
    },
    "3_10_group_desc": {
        "ru": textwrap.dedent(
            """\
            Сокращение эмоционального
            отклика на рабочие ситуации,
            неготовность активно
            общаться с другими"""
        ),
        "en": textwrap.dedent(
            """\
            Concern"""
        ),
    },
    "3_11": {
        "ru": textwrap.dedent(
            """\
            Личностная
            отстраненность"""
        ),
        "en": textwrap.dedent(
            """\
            Personal
            detachment""",
        ),
    },
    "3_11_group_desc": {
        "ru": textwrap.dedent(
            """\
            Обесценивание рабочих задач,
            агрессия на стандартные
            рабочие ситуации ("ненавижу",
            "не выношу", "не хочу")"""
        ),
        "en": textwrap.dedent(
            """\
            Concern"""
        ),
    },
    "3_12": {
        "ru": textwrap.dedent(
            """\
            Психосоматика"""
        ),
        "en": textwrap.dedent(
            """\
            Physical discomfort""",
        ),
    },
    "3_12_group_desc": {
        "ru": textwrap.dedent(
            """\
            Телесные неприятные
            состояния, плохое
            самочувствие, отсутствие
            сил/энергии"""
        ),
        "en": textwrap.dedent(
            """\
            Concern"""
        ),
    },
    # Short v2
    # 3_13 - 3_18
    "3_13": {
        "ru": textwrap.dedent(
            """\
            Профессиональный тупик"""
        ),
        "en": textwrap.dedent(
            """\
            Professional dead end"""
        ),
    },
    "3_13_group_desc": {
        "ru": textwrap.dedent(
            """\
            3_13_group_desc"""
        ),
        "en": textwrap.dedent(
            """\
            Concern"""
        ),
    },
    "3_14": {
        "ru": textwrap.dedent(
            """\
            Усталость от нагрузки, скорости и принципов работы"""
        ),
        "en": textwrap.dedent(
            """\
            Workload, speed and working principles fatigue"""
        ),
    },
    "3_14_group_desc": {
        "ru": textwrap.dedent(
            """\
            3_14_group_desc"""
        ),
        "en": textwrap.dedent(
            """\
            Concern"""
        ),
    },
    "3_15": {
        "ru": textwrap.dedent(
            """\
            Усталость от коммуникаций"""
        ),
        "en": textwrap.dedent(
            """\
            Communication fatigue"""
        ),
    },
    "3_15_group_desc": {
        "ru": textwrap.dedent(
            """\
            3_15_group_desc"""
        ),
        "en": textwrap.dedent(
            """\
            Concern"""
        ),
    },
    "3_16": {
        "ru": textwrap.dedent(
            """\
            Уход от коммуникаций"""
        ),
        "en": textwrap.dedent(
            """\
            Emotional defense """
        ),
    },
    "3_16_group_desc": {
        "ru": textwrap.dedent(
            """\
            3_16_group_desc"""
        ),
        "en": textwrap.dedent(
            """\
            Concern"""
        ),
    },
    "3_17": {
        "ru": textwrap.dedent(
            """\
            Психосоматика"""
        ),
        "en": textwrap.dedent(
            """\
            Physical discomfort"""
        ),
    },
    "3_17_group_desc": {
        "ru": textwrap.dedent(
            """\
            3_17_group_desc"""
        ),
        "en": textwrap.dedent(
            """\
            Concern"""
        ),
    },
    "3_18": {
        "ru": textwrap.dedent(
            """\
            Сокращение внимания"""
        ),
        "en": textwrap.dedent(
            """\
            Personal detachment"""
        ),
    },
    "3_18_group_desc": {
        "ru": textwrap.dedent(
            """\
            3_18_group_desc"""
        ),
        "en": textwrap.dedent(
            """\
            Concern"""
        ),
    },
    # Values
    "Section V": {
        "en": "Section V",
        "ru": "Ценности",
    },
    "Section V_text": {
        "ru": (
            "Ниже приведено исследование жизненных ценностей — универсальных человеческих потребностей, определяющих "
            "выборы и предпочтения индивида, его жизненную стратегию."
        ),
        "en": (
            "The following scores reflect life values - fundamental human needs that determine personal choices "
            "life strategies."
        ),
    },
    "Creating harmony": {
        "ru": textwrap.dedent(
            """\
            Создание гармонии"""
        ),
        "en": textwrap.dedent(
            """\
            Creating harmony"""
        ),
    },
    "Overcoming resistance": {
        "ru": textwrap.dedent(
            """\
            Преодоление"""
        ),
        "en": textwrap.dedent(
            """\
            Overcoming resistance"""
        ),
    },
    # 4_1 - 4_10
    "4_1": {
        "ru": textwrap.dedent(
            """\
            Причастность"""
        ),
        "en": textwrap.dedent(
            """\
            Affiliation"""
        ),
    },
    "4_1_group_desc": {
        "ru": textwrap.dedent(
            """\
            Потребность в выстраивании
            социальных контактов и
            ощущении принадлежности
            к группе"""
        ),
        "en": textwrap.dedent(
            """\
            Affiliation"""
        ),
    },
    "4_2": {
        "ru": textwrap.dedent(
            """\
            Традиционализм"""
        ),
        "en": textwrap.dedent(
            """\
            Conventionality"""
        ),
    },
    "4_2_group_desc": {
        "ru": textwrap.dedent(
            """\
            Уважение и следование
            нормам, принятым в
            культуре / социальной
            группе"""
        ),
        "en": textwrap.dedent(
            """\
            Affiliation"""
        ),
    },
    "4_3": {
        "ru": textwrap.dedent(
            """\
            Жажда
            впечатлений"""
        ),
        "en": textwrap.dedent(
            """\
            Sensation
            seeking"""
        ),
    },
    "4_3_group_desc": {
        "ru": textwrap.dedent(
            """\
            Потребность в разнообразии,
            новизне и глубоких
            переживаниях; желание
            погружаться в приключения,
            получать новый опыт"""
        ),
        "en": textwrap.dedent(
            """\
            Affiliation"""
        ),
    },
    "4_4": {
        "ru": textwrap.dedent(
            """\
            Эстетичность"""
        ),
        "en": textwrap.dedent(
            """\
            Aesthetic"""
        ),
    },
    "4_4_group_desc": {
        "ru": textwrap.dedent(
            """\
            Потребность в самовыражении,
            ощущение важности
            визуальности и гармоничности"""
        ),
        "en": textwrap.dedent(
            """\
            Affiliation"""
        ),
    },
    "4_5": {
        "ru": textwrap.dedent(
            """\
            Гедонизм"""
        ),
        "en": textwrap.dedent(
            """\
            Hedonism"""
        ),
    },
    "4_5_group_desc": {
        "ru": textwrap.dedent(
            """\
            Потребность в наслаждении
            или чувственном удовольствии,
            ощущении полноты жизни"""
        ),
        "en": textwrap.dedent(
            """\
            Affiliation"""
        ),
    },
    "4_6": {
        "ru": textwrap.dedent(
            """\
            Признание"""
        ),
        "en": textwrap.dedent(
            """\
            Recognition"""
        ),
    },
    "4_6_group_desc": {
        "ru": textwrap.dedent(
            """\
            Фокус на достижении
            социального статуса или
            престижа, контроля или
            доминирования над
            ресурсами и людьми"""
        ),
        "en": textwrap.dedent(
            """\
            Affiliation"""
        ),
    },
    "4_7": {
        "ru": textwrap.dedent(
            """\
            Достижения"""
        ),
        "en": textwrap.dedent(
            """\
            Achievement"""
        ),
    },
    "4_7_group_desc": {
        "ru": textwrap.dedent(
            """\
            Желание достичь личного успеха
            через соревновательность
            и преодоление «вызовов»,
            стремление быть лучшим"""
        ),
        "en": textwrap.dedent(
            """\
            Affiliation"""
        ),
    },
    "4_8": {
        "ru": textwrap.dedent(
            """\
            Коммерческий
            подход"""
        ),
        "en": textwrap.dedent(
            """\
            Commercial
            attitude"""
        ),
    },
    "4_8_group_desc": {
        "ru": textwrap.dedent(
            """\
            Принятие ответственности за
            бизнес-результаты, интерес
            к запуску продуктов"""
        ),
        "en": textwrap.dedent(
            """\
            Affiliation"""
        ),
    },
    "4_9": {
        "ru": textwrap.dedent(
            """\
            Безопасность"""
        ),
        "en": textwrap.dedent(
            """\
            Safety"""
        ),
    },
    "4_9_group_desc": {
        "ru": textwrap.dedent(
            """\
            Стремление к предсказуемости,
            структуре и порядку;
            потребность ощущать стабильность"""
        ),
        "en": textwrap.dedent(
            """\
            Affiliation"""
        ),
    },
    "4_10": {
        "ru": textwrap.dedent(
            """\
            Интеллект"""
        ),
        "en": textwrap.dedent(
            """\
            Curiosity"""
        ),
    },
    "4_10_group_desc": {
        "ru": textwrap.dedent(
            """\
            Наращивание экспертизы и
            интеллектуального потенциала,
            созданию сложных
            интеллектуальных решений"""
        ),
        "en": textwrap.dedent(
            """\
            Affiliation"""
        ),
    },
    # Team Report
    "Team Report": {
        "ru": "Командный отчет",
        "en": "Team Report",
    },
    "Project": {
        "ru": "Проект:",
        "en": "Project:",
    },
    "group_report_description": {
        "ru": (
            "Модель описывает четыре управленческие роли. Выполнение каждой из них помогает команде или организации обеспечить "
            "максимально эффективную деятельность. Роли распределяются исходя из особенностей характера и интуйтивных предпочтений в "
            "работе (ценности, убеждения, мотиваторы). Сотрудник может совмещать одну или несколько ролей. При этом в матрице ролей "
            "будет указываться доминантная роль."
        ),
        "en": (
            "Based on decades of academic research Zetic has developed a tool for scientific personality measurement "
            "for business. The tool can be used for a variety of recruitment and development purposes. The approach was "
            "tested on a large sample of executives over several years. Our study of resilience and stress behavior has "
            "become the largest in Russia over the past 15 years. Zetic 4S questionnaire consists of:"
        ),
    },
    "Предприниматель": {
        "ru": "Предприниматель",
        "en": "Entrepreneur",
    },
    "Предприниматель Описание": {
        "ru": (
            "**Предприниматель** – роль направлена на формирование и реализацию долгосрочных планов / стратегии, обеспечение"
            " развития бизнеса и продуктов. Сотрудникам в этой роли свойственно глубоко погружаться в предметную"
            " область, развивать экспертизу, разрабатывать и предлагать варианты развития бизнеса (клиентов, продуктов,"
            " вариантов монетизации, новых рыночных ниш и т.д.). Им свойственно фокусироваться на идеях, "
            "ориентироваться на поиск новых/интересных решений, фантазировать. Они комфортно переживают перемены и эксперименты."
        ),
        "en": (
            "Based on decades of academic research Zetic has developed a tool for scientific personality measurement "
            "for business. The tool can be used for a variety of recruitment and development purposes. The approach was "
            "tested on a large sample of executives over several years. Our study of resilience and s"
            "tress behavior has "
            "become the largest in Russia over the past 15 years. Zetic 4S questionnaire consists of:"
        ),
    },
    "Предприниматель Подробнее": {
        "ru": textwrap.dedent(
            """\
            • Контролер – практичный, инициативный, высокоорганизованный и целеустремленный. Имеет твердые жизненные убеждения и старается жить и работать согласно своим высоким стандартам. Эффективно управляет работой, планирует и последовательно работает на развитие бизнеса. Держит свои обещания и ждут этого от других.
            • Изобретатель – обладает острым умом, широкой базой познаний и способностью объединять разрозненные элементы в единые решения. Находится в постоянном поиске знаний, создания сложных интеллектуальных решений, готов подвергать сомнению общепринятый образ мышления. Не практичен, не терпит рутины. Недисциплинирован, выполняет задачи скачкообразно.
            • Аналитик – обладает аналитическим мышлением, четко видит будущее и стремится реализовывать процессы максимально эффективно. Настойчив, упрям, ориентирован на развитие, может не уделять внимание чувствам и переживаниям других.
            • Искатель ресурсов - авантюрный, активный, быстрый. Легко ориентируется в мелких деталях, фактах, цифрах. "Недисциплинирован, может отклоняться от плана, способен эффективно действовать в экстремальных ситуациях, исправляет свои ошибки по пути.  Проницателен, быстро считывает пространство и людей, подстраивается под изменения."""
        ),
        "en": textwrap.dedent(
            """\
        • The section K measures the basic personality traits and its influence of business behavior and performance.
        • The section С describes the basic reactions on stress, actions taken by a person to cope with the new worries, to adapt to tension and to find a way out of a traumatic situation.
        • The section B reflects the psychological factors that lead to burnout, the burnout indicator and intensity.
        • The section V describes the universal well-established needs and life priorities of the individual that influence decisions and choices."""
        ),
    },
    "Производитель": {
        "ru": "Производитель",
        "en": "",
    },
    "Производитель Описание": {
        "ru": (
            "**Производитель** – роль обеспечивает результативность в краткосрочном аспекте. Действия направлены "
            "на решение операционных «горящих» задач максимально быстро. Сотрудники в этой роли проявляют нетерпеливость, "
            "продуктивность и прагматичность, внутреннюю жесткость. Предрасположены к действию больше, чем к размышлениям и "
            "анализу. Склонны действовать по одиночке. Получают удовлетворение от собственной вовлеченности в работу и достижения результатов."
        ),
        "en": "",
    },
    "Производитель Подробнее": {
        "ru": textwrap.dedent(
            """\
            • Организатор – фокусируется на последовательном выполнении задач, предпочитает ясность и четкую организацию. Склонен игнорировать чувства в пользу логики и фактов. Ориентируется в мелких деталях и цифрах. Способен четко и внимательно контролировать работу и результаты.
            • Любитель улучшений – рациональный, логичный, целеустремленный. Стремится к совершенству систем и процессов, ориентирован на поиск возможностей для улучшений, высокопродуктивен. Склонен игнорировать чувства в пользу фактов и цифр. Быстро принимает решения и реализует их, четко организует работу команды.
            • Решатель проблем - проявляется как высокомерный и критичный к другим. Действует скачкообразно, может отклоняться от плана. Находит быстрые, элегантные решения сложных задач. Нацелен на действие, а не на коммуникации.
            • Исполнитель - погружен в предметную область, прагматичен, стремится понять логику и механизм работы. С удовольствием сам будет выполнять работу и включаться в детали, делиться опытом с другими. Настойчив, доводитработу до конца. Слонен быть недисциплинированным, достигать цели в последний момент.""",
        ),
        "en": "",
    },
    "Администратор": {
        "ru": "Администратор",
        "en": "",
    },
    "Администратор Описание": {
        "ru": (
            "**Администратор – роль обеспечивает эффективность, технологичность, стандартизацию в краткосрочном аспекте. "
            "Этим сотрудникам свойственно унифицировать работу, структурировать информацию и процессы, следить за порядком, "
            "согласовывать и поддерживать единые правила работы. Как правило они стремятся мыслить линейно, действовать "
            "осторожно и дисциплинировано, обращать внимание на мелкие детали."
        ),
        "en": "",
    },
    "Администратор Подробнее": {
        "ru": textwrap.dedent(
            """\
            • __Хранитель__ – обладает развитыми навыками общения, считывает пространство и команду, чуток к состоянию команды.Внимателен к деталям, мыслит от частного к общему, педантичен, проявляет перфекционизм. Воспринимает рабочие обязанности как личную ответственность, стремится выполнять их больше и лучше, чем ожидается.
            • __Вдохновитель__ – чуткий и проницательный, вносит гармонию в общение между людьми. Склонен идеализировать мир, верить в счастливое будущее. Ориентируется на формирование экологичных, гуманистичных, системных решений. Действует дисциплинировано и аккуратно.
            • __Опекун__ – обладает художественным восприятием и развитым вкусом, открыт к изменениям и экспериментам, не любит рутину. Находит правильные слова для создания доверительной коммуникации, выстраивает теплое общение с другими, чуток и тактичен. Готов поддерживать и помогать в развитии другим.
            • __Благородный служитель__ – формирует глубокую и продуманную систему моральных принципов и долга. Обладает очень хорошей интуицией и творческим чутьем. Располагает к себе, сглаживает острые углы. Ценит возможность быть частью коллектива и может жертвовать своими интересами ради других. Проявляется как вдумчивый, но не дистиллированный и непоследовательный.""",
        ),
        "en": "",
    },
    "Интегратор": {
        "ru": "Интегратор",
        "en": "",
    },
    "Интегратор Описание": {
        "ru": (
            "**Интегратор** – роль направлена на создание целостной организации, формирование единого видения, "
            "правильного организационного климата и культуры, системы ценностей, которые будут стимулировать людей действовать"
            " сообща, позволят вплетать цели каждого в цели группы и бизнеса в целом. Представители этой роли социально активны, "
            "стремятся к коммуникации и кросс-функциональному взаимодействию, склонны к эмпатии, умеют выслушать и поддержать, "
            "формируют атмосферу взаимного уважения в коллективе."
        ),
        "en": "",
    },
    "Интегратор Подробнее": {
        "ru": textwrap.dedent(
            """\
                    • **Массовик-затейник** – стремится быть в центре внимания, принимает на себя лидерскую роль, пользуется поддержкой других. Практичный, внимательный к деталям. Умеет планировать и дисциплинировано реализовывать работу.
                    • **Чуткий наставник** - выстраивает крепкие отношения с коллегами, заботится о людях. Мыслит широко и интуитивно. Умеет планировать и дисциплинировано реализовывать работу. Формирует эффективные процессы, в которых люди могут комфортно работать.
                    • **Развлекатель** – практичный, оптимистичный, спонтанный. Воспринимает мир и работу как игру, воодушевляет этим окружающих. Легко адаптируется к переменам, решает проблемы по мере их возникновения. Наблюдателен и прозорлив, тонко чувствует состояние людей, проявляет активный интерес и всегда готов прийти на помощь.
                    • **Мотиватор** - открыт, любит говорить о людях и делиться планами. С удовольствием обсуждает собственные смелые идеи и фантазии. Ищет свободы, спонтанности и возможности для творчества. Склонен смотреть на жизнь как на большую сложную головоломку, видеть ее через призму интуиции, эмоций, сострадания, всегда пытается добиться более глубокого понимания.""",
        ),
        "en": "",
    },
    "": {
        "ru": "",
        "en": "",
    },
}
DEFAULT_LANG = "en"


class TranslationDict:
    def __init__(self, translations: Dict[str, Dict[str, str]]):
        self._dict = translations

    def get_translation(self, key: str, lang: str = DEFAULT_LANG):
        if key not in self._dict:
            return key
        if lang in self._dict[key]:
            return self._dict[key][lang]
        elif DEFAULT_LANG in self._dict[key]:
            return self._dict[key][DEFAULT_LANG]
        else:
            return key


TRANSLATIONS_DICT = TranslationDict(TRANSLATIONS)
